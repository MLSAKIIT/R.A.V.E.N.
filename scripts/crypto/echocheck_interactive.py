#!/usr/bin/env python3
"""
echocheck_interactive.py
Interactive file/text encoder & decoder.

Usage:
    python3 echocheck_interactive.py
"""

import os
import sys
import base64   
import codecs
import urllib.parse
import logging
from pathlib import Path
from datetime import datetime
from typing import Optional
import itertools
import time
import fnmatch

# --------------------------
# Logging & Colors
# --------------------------
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
class C:
    RED = "\033[91m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    CYAN = "\033[96m"
    BOLD = "\033[1m"
    RESET = "\033[0m"

def info(msg: str):
    print(f"{C.CYAN}{msg}{C.RESET}")

def ok(msg: str):
    print(f"{C.GREEN}{msg}{C.RESET}")

def warn(msg: str):
    print(f"{C.YELLOW}{msg}{C.RESET}")

def err(msg: str):
    print(f"{C.RED}{msg}{C.RESET}")

# --------------------------
# Encoding / Decoding (bytes)
# --------------------------
def b64_encode_bytes(data: bytes) -> bytes:
    return base64.b64encode(data)

def b64_decode_bytes(data: bytes) -> Optional[bytes]:
    try:
        return base64.b64decode(data, validate=True)
    except Exception:
        return None

def hex_encode_bytes(data: bytes) -> bytes:
    return data.hex().encode("ascii")

def hex_decode_bytes(data: bytes) -> Optional[bytes]:
    try:
        # ensure data is ascii hex text
        return bytes.fromhex(data.decode("ascii"))
    except Exception:
        return None

# rot13/url are text-only (operate on str)
def rot13_text(s: str) -> str:
    return codecs.encode(s, "rot_13")

def url_encode_text(s: str) -> str:
    return urllib.parse.quote(s)

def url_decode_text(s: str) -> str:
    return urllib.parse.unquote(s)

# --------------------------
# Helpers: detection & printable check
# --------------------------
def is_mostly_printable(b: bytes, threshold: float = 0.95) -> bool:
    """Return True if a large fraction of characters are printable (after utf-8 decode)."""
    try:
        s = b.decode("utf-8")
    except Exception:
        return False
    if not s:
        return True
    printable = sum(1 for ch in s if ch.isprintable() or ch.isspace())
    return (printable / len(s)) >= threshold

def detect_encoding_bytes(data: bytes) -> Optional[str]:
    """
    Attempt to detect encoding of `data` (which is the raw bytes of the file).
    Returns 'base64', 'hex', 'url', 'rot13' or None if unknown.
    Detection strategy:
      - Try base64 decode with validation, check result is mostly printable -> base64
      - Try hex decode and check printable -> hex
      - If bytes decode to UTF-8 and contains %XX -> url
      - If bytes decode to UTF-8 and rot13 changes content -> rot13
    """
    # try base64
    b64_try = b64_decode_bytes(data)
    if b64_try is not None and is_mostly_printable(b64_try):
        return "base64"

    # try hex
    hex_try = hex_decode_bytes(data)
    if hex_try is not None and is_mostly_printable(hex_try):
        return "hex"

    # try url (text)
    try:
        text = data.decode("utf-8")
        if "%" in text:
            dec = url_decode_text(text)
            if dec != text:
                return "url"
    except Exception:
        pass

    # try rot13 (text)
    try:
        text = data.decode("utf-8")
        rot = rot13_text(text)
        if rot != text:
            return "rot13"
    except Exception:
        pass

    return None
# --------------------------
# Cipher Functions

def caesar(text, shift, decrypt=False):
    if decrypt:
        shift = -shift
    result = ""
    for char in text:
        if char.isalpha():
            base = ord('A') if char.isupper() else ord('a')
            result += chr((ord(char) - base + shift) % 26 + base)
        else:
            result += char
    return result

def vigenere(text, key, decrypt=False):
    key = key.lower()
    result = ""
    key_index = 0
    for char in text:
        if char.isalpha():
            shift = ord(key[key_index % len(key)]) - ord('a')
            if decrypt:
                shift = -shift
            base = ord('A') if char.isupper() else ord('a')
            result += chr((ord(char) - base + shift) % 26 + base)
            key_index += 1
        else:
            result += char
    return result

def xor_cipher(data, key):
    key_bytes = key.encode()
    result = bytes([b ^ key_bytes[i % len(key_bytes)] for i, b in enumerate(data)])
    return result


# --------------------------
# File search & IO
# --------------------------
import fnmatch

#--------encoder/decoder---------

def find_file(filename: str, root: Path = None) -> Optional[Path]:
    """
    Search recursively for a file anywhere under the user's home directory.
    Returns the first full Path match found, or None if not found.
    """

    filename = filename.strip()
    if not filename:
        err("❌ No filename provided.")
        return None

    if root is None:
        root = Path.home()

    info(f"🔍 Searching for '{filename}' in {root} and subfolders...")

    for dirpath, dirnames, filenames in os.walk(root, topdown=True):
        # Skip system directories and cache folders to avoid permission errors
        dirnames[:] = [d for d in dirnames if not d.startswith('.') and 'cache' not in d.lower()]

        for name in filenames:
            if fnmatch.fnmatch(name.lower(), filename.lower()):
                found_path = Path(dirpath) / name
                ok(f"✅ Found: {found_path}")
                return found_path

    err(f"❌ File '{filename}' not found anywhere under {root}.")
    return None


def read_file_bytes(path: Path) -> bytes:
    """Open file as bytes."""
    return path.read_bytes()

def write_file_bytes(path: Path, data: bytes):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data)

def read_text(path: Path) -> str:
    return path.read_text(errors="ignore")

def write_text(path: Path, s: str):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(s, encoding="utf-8")

# --------------------------
# Save output safely (timestamped)
# --------------------------
def make_output_path(original: Path, mode: str, encoding_type: str, outdir: Path) -> Path:
    outdir = outdir.expanduser()
    outdir.mkdir(parents=True, exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_name = f"{original.stem}_{mode}_{encoding_type}_{ts}{original.suffix or '.txt'}"
    return outdir / safe_name

# --------------------------
# Interactive flows
# --------------------------

#--------encodeing decoding
def interactive_file_mode_enco(outdir: Path):
    fname = input("Enter filename to search for (relative to cwd): ").strip()
    if not fname:
        err("No filename provided.")
        return

    file_path = find_file(fname)
    if not file_path:
        err(f"File '{fname}' not found under {Path.cwd()}.")
        return
    ok(f"Found: {file_path}")

    action = input("Encode or Decode? (e/d): ").strip().lower()
    if action not in ("e", "d"):
        err("Invalid choice.")
        return

    # read bytes (binary-safe)
    data = read_file_bytes(file_path)

    if action == "e":
        print("Choose encoding type:")
        print("1) Base64\n2) Hex\n3) ROT13 (text only)\n4) URL (text only)")
        choice = input("Enter choice (1-4): ").strip()
        typemap = {"1": "base64", "2": "hex", "3": "rot13", "4":"url"}
        encoding = typemap.get(choice)
        if not encoding:
            err("Invalid encoding choice.")
            return

        # perform encoding (bytes => bytes or text => bytes)
        if encoding in ("base64", "hex"):
            result_bytes = b64_encode_bytes(data) if encoding == "base64" else hex_encode_bytes(data)
            out_path = make_output_path(file_path, "encoded", encoding, outdir)
            # avoid overwrite: timestamp already gives uniqueness, but check anyway
            if out_path.exists():
                confirm = input(f"File exists {out_path.name}. Overwrite? (y/n): ").strip().lower()
                if confirm != "y":
                    warn("Aborted saving.")
                    return
            write_file_bytes(out_path, result_bytes)
            ok(f"Saved encoded file to: {out_path}")

        else:
            # text-only encodings: need to decode bytes -> str first
            try:
                text = data.decode("utf-8")
            except Exception:
                err("File is not valid UTF-8 text; cannot use text-only encoding.")
                return
            if encoding == "rot13":
                res_text = rot13_text(text)
            elif encoding == "url":
                res_text = url_encode_text(text)
            else:
                err("Unsupported text encoding.")
                return
            out_path = make_output_path(file_path, "encoded", encoding, outdir)
            if out_path.exists():
                confirm = input(f"File exists {out_path.name}. Overwrite? (y/n): ").strip().lower()
                if confirm != "y":
                    warn("Aborted saving.")
                    return
            write_text(out_path, res_text)
            ok(f"Saved encoded file to: {out_path}")

    else:  # decode
        detected = detect_encoding_bytes(data)
        if not detected:
            err("Unable to detect encoding automatically.")
            # offer manual decode attempt
            manual = input("Try manual decode? (base64/hex/rot13/url/none): ").strip().lower()
            if manual in ("base64","hex","rot13","url"):
                detected = manual
            else:
                return
        ok(f"Detected encoding: {detected}")

        if detected in ("base64", "hex"):
            if detected == "base64":
                decoded = b64_decode_bytes(data)
            else:
                decoded = hex_decode_bytes(data)
            if decoded is None:
                err("Decoding failed or data invalid.")
                return
            out_path = make_output_path(file_path, "decoded", detected, outdir)
            if out_path.exists():
                confirm = input(f"File exists {out_path.name}. Overwrite? (y/n): ").strip().lower()
                if confirm != "y":
                    warn("Aborted saving.")
                    return
            write_file_bytes(out_path, decoded)
            ok(f"Saved decoded file to: {out_path}")

        elif detected in ("rot13", "url"):
            # text-only decodes
            try:
                text = data.decode("utf-8")
            except Exception:
                err("File is not valid UTF-8 text; cannot use text-only decoding.")
                return
            if detected == "rot13":
                out_text = rot13_text(text)
            else:
                out_text = url_decode_text(text)
            out_path = make_output_path(file_path, "decoded", detected, outdir)
            if out_path.exists():
                confirm = input(f"File exists {out_path.name}. Overwrite? (y/n): ").strip().lower()
                if confirm != "y":
                    warn("Aborted saving.")
                    return
            write_text(out_path, out_text)
            ok(f"Saved decoded file to: {out_path}")

        else:
            err("Unsupported detected type.")

def interactive_text_mode_enco(outdir: Path):
    text = input("Enter text: ")
    if text is None:
        err("No text entered.")
        return
    action = input("Encode or Decode? (e/d): ").strip().lower()
    if action not in ("e", "d"):
        err("Invalid choice.")
        return

    if action == "e":
        print("Choose encoding type:")
        print("1) Base64\n2) Hex\n3) ROT13\n4) URL")
        choice = input("Enter choice (1-4): ").strip()
        typemap = {"1":"base64", "2":"hex", "3":"rot13", "4":"url"}
        encoding = typemap.get(choice)
        if not encoding:
            err("Invalid choice.")
            return
        if encoding == "base64":
            ok(base64.b64encode(text.encode()).decode())
        elif encoding == "hex":
            ok(text.encode().hex())
        elif encoding == "rot13":
            ok(rot13_text(text))
        elif encoding == "url":
            ok(url_encode_text(text))

    else:
        # decode: attempt auto detect
        # use bytes for detection
        data = text.encode()
        detected = detect_encoding_bytes(data)
        if not detected:
            err("Could not detect encoding of the provided text.")
            return
        ok(f"Detected encoding: {detected}")
        try:
            if detected == "base64":
                dec = b64_decode_bytes(data).decode()
            elif detected == "hex":
                dec = hex_decode_bytes(data).decode()
            elif detected == "rot13":
                dec = rot13_text(text)
            elif detected == "url":
                dec = url_decode_text(text)
            else:
                err("Unsupported detected encoding.")
                return
            ok(dec)
        except Exception as e:
            err(f"Decoding error: {e}")

def interactive_encoder_decoder(outdir: Path):
    while True:
        print()
        info("🎧 Encore Encoder — Encode / Decode Anything")
        print("1) File Encode/Decode")
        print("2) Text Encode/Decode")
        print("3) Back to Main Menu")
        choice = input("Enter choice (1-3): ").strip()

        if choice == "1":
            interactive_file_mode_enco(outdir)
        elif choice == "2":
            interactive_text_mode_enco(outdir)
        elif choice == "3":
            ok("Returning to main menu...")
            break
        else:
            warn("Invalid choice. Please try again.")

#-------Cipher tools--------

def interactive_cipher_mode(outdir: Path):
    info("🔐 Cipher/Decipher Mode")
    mode = input("Encrypt or Decrypt? (e/d): ").strip().lower()
    decrypt = mode == "d"

    print("Choose Cipher:")
    print("1) Caesar\n2) Vigenère\n3) XOR")
    choice = input("Enter choice (1-3): ").strip()

    t_or_f = input("Work with text or file? (t/f): ").strip().lower()

    if t_or_f == "t":
        text = input("Enter text: ")

        if choice == "1":
            shift = int(input("Enter shift (1-25): "))
            result = caesar(text, shift, decrypt)
        elif choice == "2":
            key = input("Enter key (letters only): ")
            result = vigenere(text, key, decrypt)
        elif choice == "3":
            key = input("Enter key: ")
            result = xor_cipher(text.encode(), key).decode(errors="ignore")
        else:
            err("Invalid cipher choice.")
            return

        ok("\nResult:")
        print(result)

    elif t_or_f == "f":
        filename = input("Enter filename to search for: ").strip()
        file_path = find_file(filename)
        if not file_path:
            err("File not found!")
            return

        with open(file_path, "rb") as f:
            data = f.read()

        if choice == "3":  # XOR for binary
            key = input("Enter key: ")
            result = xor_cipher(data, key)
            out_path = outdir / f"{file_path.stem}_{'dec' if decrypt else 'enc'}_xor{file_path.suffix}"
            out_path.write_bytes(result)
            ok(f"Saved XOR {'decrypted' if decrypt else 'encrypted'} file to: {out_path}")
        else:
            try:
                text = data.decode("utf-8")
            except Exception:
                err("File not text. Use XOR for binary.")
                return

            if choice == "1":
                shift = int(input("Enter shift (1-25): "))
                result = caesar(text, shift, decrypt)
                name = "caesar"
            elif choice == "2":
                key = input("Enter key: ")
                result = vigenere(text, key, decrypt)
                name = "vigenere"
            else:
                err("Invalid choice.")
                return

            out_path = outdir / f"{file_path.stem}_{'dec' if decrypt else 'enc'}_{name}{file_path.suffix}"
            out_path.write_text(result)
            ok(f"Saved result to: {out_path}")
    else:
        err("Invalid option.")

#--------Hashing--------------
import hashlib

def _hash_file_chunks(path: Path, algo: str = "sha256", chunk_size: int = 8 * 1024 * 1024) -> str:
    """
    Compute hash of a file by reading in chunks.
    Returns hex digest.
    """
    algo = algo.lower()
    if algo == "blake2b":
        h = hashlib.blake2b()
    else:
        if not hasattr(hashlib, algo):
            raise ValueError(f"Unsupported algorithm: {algo}")
        h = getattr(hashlib, algo)()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(chunk_size), b""):
            h.update(chunk)
    return h.hexdigest()

def interactive_hashing(outdir: Optional[Path] = None):
    """
    Interactive version of hashing tool.
    Lets the user choose file or text, picks algorithm,
    finds file automatically if needed, and saves digest.
    """
    import hashlib
    outdir = Path(outdir) if outdir else (Path.home() / "echocheck")
    outdir.mkdir(parents=True, exist_ok=True)

    print("🔢 Hector the Hasher — Hash anything securely!")
    user_input = input("📂 Enter filename to hash (or type text directly): ").strip()
    if not user_input:
        err("No input provided.")
        return

    # Detect whether input is file or plain text
    file_path = None
    candidate = Path(user_input).expanduser()
    if candidate.exists():
        file_path = candidate
    else:
        found = find_file(user_input)
        if found:
            file_path = found
        else:
            ok("Treating input as plain text.")
    
    algo = input("Choose algorithm (md5 / sha1 / sha256 / sha512 / blake2b): ").lower().strip()
    supported = {"md5", "sha1", "sha256", "sha512", "blake2b"}
    if algo not in supported:
        err("Unsupported algorithm.")
        return

    if file_path:
        ok(f"📁 Hashing file: {file_path} using {algo.upper()}")
        try:
            digest = _hash_file_chunks(file_path, algo)
        except Exception as e:
            err(f"Error hashing file: {e}")
            return
        name = file_path.stem
        data_type = "file"
    else:
        ok(f"📝 Hashing text using {algo.upper()}")
        h = getattr(hashlib, algo)() if algo != "blake2b" else hashlib.blake2b()
        h.update(user_input.encode("utf-8"))
        digest = h.hexdigest()
        name = "text"
        data_type = "text"

    ok(f"🔐 {algo.upper()}({data_type}) = {digest}")

    # Save hash digest
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    fname = f"{name}_{algo}_{ts}.txt"
    target = outdir / fname
    target.write_text(digest, encoding="utf-8")
    ok(f"💾 Saved digest to: {target}")

#--------enpcrypter decrypter----------
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
import secrets

def interactive_encryptor(outdir: Path):
    """
    AES-based encryption/decryption tool.
    Uses PBKDF2 key derivation and AES-GCM mode for strong protection.
    """
    try:
        import base64

        print()
        print("Choose mode:")
        print("1) Encrypt file")
        print("2) Decrypt file")
        mode = input("Enter choice (1-2): ").strip()

        if mode not in ("1", "2"):
            err("Invalid choice.")
            return

        filename = input("Enter filename to search for: ").strip()
        file_path = find_file(filename)
        if not file_path:
            err(f"File '{filename}' not found anywhere in your system.")
            return
        ok(f"Found: {file_path}")

        password = input("Enter password: ").strip().encode()
        if not password:
            err("Password cannot be empty.")
            return

        # Derive key from password
        salt = secrets.token_bytes(16)
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
            backend=default_backend()
        )
        key = kdf.derive(password)

        data = read_file_bytes(file_path)

        if mode == "1":  # Encrypt
            nonce = secrets.token_bytes(12)
            cipher = Cipher(algorithms.AES(key), modes.GCM(nonce), backend=default_backend())
            encryptor = cipher.encryptor()
            ciphertext = encryptor.update(data) + encryptor.finalize()

            enc_blob = salt + nonce + encryptor.tag + ciphertext
            out_path = make_output_path(file_path, "encrypted", "aes", outdir).with_suffix(".enc")
            write_file_bytes(out_path, enc_blob)
            ok(f"✅ Encrypted and saved to: {out_path}")

        else:  # Decrypt
            try:
                salt = data[:16]
                nonce = data[16:28]
                tag = data[28:44]
                ciphertext = data[44:]

                # Rebuild key from password + salt
                kdf = PBKDF2HMAC(
                    algorithm=hashes.SHA256(),
                    length=32,
                    salt=salt,
                    iterations=100000,
                    backend=default_backend()
                )
                key = kdf.derive(password)

                cipher = Cipher(algorithms.AES(key), modes.GCM(nonce, tag), backend=default_backend())
                decryptor = cipher.decryptor()
                plaintext = decryptor.update(ciphertext) + decryptor.finalize()

                out_path = make_output_path(file_path, "decrypted", "aes", outdir)
                write_file_bytes(out_path, plaintext)
                ok(f"✅ Decrypted and saved to: {out_path}")

            except Exception as e:
                err(f"❌ Decryption failed: {e}")

    except KeyboardInterrupt:
        warn("Interrupted by user.")

#-----------Hash Cracker------------

import hashlib
import itertools
import time
from typing import Optional, Iterable

def interactive_crack_hash(
    target_hash: str,
    algo: str = "md5",
    dictionary_path: Optional[Path] = None,
    do_bruteforce: bool = False,
    charset: str = "abcdefghijklmnopqrstuvwxyz0123456789",
    min_len: int = 1,
    max_len: int = 4,
    salt: Optional[str] = None,
    salt_position: str = "suffix",  # "prefix" | "suffix" | "none"
    case_variants: bool = False,
    show_progress: bool = True,
    max_attempts: Optional[int] = None,
) -> Optional[str]:
    """
    Try to recover the plaintext for `target_hash` using a dictionary attack
    and optionally a brute-force attack.

    Parameters
    ----------
    target_hash : str
        Hex digest string to crack.
    algo : str
        Hash algorithm name (md5, sha1, sha256, sha512).
    dictionary_path : Optional[Path]
        Path to a newline-separated wordlist file to try first (dictionary attack).
    do_bruteforce : bool
        If True, run brute-force after dictionary (use with care).
    charset : str
        Characters to use for brute-force generation.
    min_len, max_len : int
        Minimum/maximum length for brute-forcing.
    salt : Optional[str]
        If not None, treat candidate as salted; salt_position controls where salt is applied.
    salt_position : str
        "prefix", "suffix", or "none"
    case_variants : bool
        If True and dictionary is used, also try simple case variants (lower, upper, capitalize).
    show_progress : bool
        Print status updates.
    max_attempts : Optional[int]
        Stop after this many attempts (None = unlimited).

    Returns
    -------
    Optional[str]
        The recovered plaintext if found, otherwise None.
    """

    target_hash = target_hash.strip().lower()
    algo = algo.lower()

    # Validate algorithm
    if not hasattr(hashlib, algo):
        err(f"Unsupported hash algorithm: {algo}")
        return None

    hasher_factory = lambda: getattr(hashlib, algo)()

    def hash_candidate(candidate: str) -> str:
        """Return hexdigest for candidate with optional salt placement."""
        if salt and salt_position == "prefix":
            data = (salt + candidate).encode("utf-8")
        elif salt and salt_position == "suffix":
            data = (candidate + salt).encode("utf-8")
        else:
            data = candidate.encode("utf-8")
        h = hasher_factory()
        h.update(data)
        return h.hexdigest()

    attempts = 0
    start_time = time.time()

    # --- Helper to check candidate and report ---
    def try_candidate(cand: str) -> Optional[str]:
        nonlocal attempts
        attempts += 1
        if max_attempts is not None and attempts > max_attempts:
            return None
        digest = hash_candidate(cand)
        if digest == target_hash:
            return cand
        return None

    # --- DICTIONARY ATTACK ---
    if dictionary_path:
        if show_progress:
            info(f"🔎 Starting dictionary attack using: {dictionary_path}")
        try:
            with open(dictionary_path, "r", errors="ignore") as wf:
                for raw in wf:
                    word = raw.rstrip("\n\r")
                    if not word:
                        continue

                    # Try the word itself
                    found = try_candidate(word)
                    if found:
                        if show_progress:
                            ok(f"✅ Found (dictionary): {found} after {attempts} attempts")
                        return found

                    # Common case variants if asked
                    if case_variants:
                        for cand in (word.lower(), word.upper(), word.capitalize()):
                            if cand == word:  # already tried
                                continue
                            found = try_candidate(cand)
                            if found:
                                if show_progress:
                                    ok(f"✅ Found (dictionary variant): {found} after {attempts} attempts")
                                return found

                    # Optionally try simple numeric suffixes (common passwords like pass123)
                    # (keep this optional/disabled for speed / uncomment if desired)
                    # for n in range(0, 100):
                    #     found = try_candidate(f"{word}{n}")
                    #     if found:
                    #         return found

                    # Print progress occasionally
                    if show_progress and attempts % 5000 == 0:
                        elapsed = time.time() - start_time
                        rate = attempts / elapsed if elapsed > 0 else 0
                        print(f"... tried {attempts} candidates, {rate:.1f} tries/sec")
        except FileNotFoundError:
            err(f"Wordlist file not found: {dictionary_path}")
        except Exception as e:
            err(f"Dictionary attack error: {e}")

    # If we got here and found nothing, proceed to brute-force if requested
    if do_bruteforce:
        if show_progress:
            info("🔎 Starting brute-force attack (this can be very slow!)")
            info(f"Charset length={len(charset)} min_len={min_len} max_len={max_len}")

        total_attempts_est = sum(len(charset) ** L for L in range(min_len, max_len + 1))
        if show_progress:
            warn(f"Estimated attempts: ~{total_attempts_est:,} (do not run large lengths)")

        # Iterate lengths
        try:
            for L in range(min_len, max_len + 1):
                if show_progress:
                    info(f"-- Trying length {L} --")
                for prod in itertools.product(charset, repeat=L):
                    cand = "".join(prod)
                    found = try_candidate(cand)
                    if found:
                        if show_progress:
                            ok(f"✅ Found (bruteforce): {found} after {attempts} attempts")
                        return found
                    # occasionally print status
                    if show_progress and attempts % 100000 == 0:
                        elapsed = time.time() - start_time
                        rate = attempts / elapsed if elapsed > 0 else 0
                        print(f"... tried {attempts} candidates, {rate:.1f} tries/sec")
                    if max_attempts is not None and attempts >= max_attempts:
                        warn("Max attempts reached, stopping.")
                        return None
        except KeyboardInterrupt:
            warn("Interrupted by user during brute-force.")
            return None
        except Exception as e:
            err(f"Brute-force error: {e}")
            return None

    # If nothing found
    if show_progress:
        elapsed = time.time() - start_time
        info(f"Finished. Attempts: {attempts} Time: {elapsed:.1f}s")
    return None
#wrapper 
def interactive_crack_hash_cli(outdir: Optional[Path] = None):
    """
    Interactive CLI wrapper that prompts the user for the target hash and options,
    then calls the core interactive_crack_hash(...) function.
    """
    outdir = Path(outdir) if outdir else (Path.home() / "echocheck")
    try:
        target_hash = input("Enter target hash (hex digest): ").strip()
        if not target_hash:
            err("No target hash provided.")
            return

        algo = input("Algorithm (md5 / sha1 / sha256 / sha512) [md5]: ").strip().lower() or "md5"
        if algo not in ("md5", "sha1", "sha256", "sha512"):
            err("Unsupported algorithm.")
            return

        dict_path_input = input("Wordlist path (leave blank to skip dictionary attack): ").strip()
        dictionary_path = Path(dict_path_input) if dict_path_input else None

        brute = input("Also run brute-force after dictionary? (y/N): ").strip().lower() == "y"
        charset = input("Brute-force charset (default: lowercase+digits): ").strip()
        if not charset:
            charset = "abcdefghijklmnopqrstuvwxyz0123456789"

        min_len_input = input("Brute min length [1]: ").strip() or "1"
        max_len_input = input("Brute max length [4]: ").strip() or "4"
        try:
            min_len = int(min_len_input)
            max_len = int(max_len_input)
        except ValueError:
            err("Invalid min/max lengths.")
            return
        if min_len < 1 or max_len < min_len:
            err("Invalid length range.")
            return

        salt = input("Salt (if any, leave blank for none): ").strip() or None
        salt_position = "suffix"
        if salt:
            sp = input("Salt position (prefix/suffix) [suffix]: ").strip().lower()
            if sp in ("prefix", "suffix"):
                salt_position = sp

        case_variants = input("Try case variants for dictionary words? (y/N): ").strip().lower() == "y"
        max_attempts_input = input("Max attempts (press Enter for unlimited): ").strip()
        max_attempts = int(max_attempts_input) if max_attempts_input.isdigit() else None

        ok("Starting attack... (press Ctrl-C to stop brute-force early)")
        found = interactive_crack_hash(
            target_hash=target_hash,
            algo=algo,
            dictionary_path=dictionary_path,
            do_bruteforce=brute,
            charset=charset,
            min_len=min_len,
            max_len=max_len,
            salt=salt,
            salt_position=salt_position,
            case_variants=case_variants,
            show_progress=True,
            max_attempts=max_attempts,
        )

        if found:
            ok(f"✅ Hash cracked: {found}")
            # Save recovered plaintext
            if outdir:
                outdir.mkdir(parents=True, exist_ok=True)
                fn = outdir / f"cracked_{algo}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
                fn.write_text(found, encoding="utf-8")
                ok(f"Saved recovered plaintext to: {fn}")
        else:
            warn("No match found.")

    except KeyboardInterrupt:
        warn("Interrupted by user.")



# --------------------------
# Main interactive loop
# --------------------------
def main_loop():
    outdir = Path.home() / "echocheck"
    info("========================================")
    info("🔐 EchoCheck — Interactive Encoder/Decoder")
    info("========================================")
    warn(f"Outputs will be saved to: {outdir}")
    info("LoCkEd & LoAdEd!!!")

    try:
        while True:
            print()
            print("Choose mode:")
            print("1) Encore Encoder&Decoder")
            print("2) Hush hashing tool")
            print("3) cyphy cipher tool")
            print("4) Encore Encryptor/Decryptor")
            print("5) Hector the hash cracker")
            print("6) Quit")
            mode = input("Enter choice (1-6): ").strip()
            if mode == "1":
                interactive_encoder_decoder(outdir)
            elif mode == "2":
                interactive_hashing(outdir)
            elif mode == "3":
                interactive_cipher_mode(outdir)
            elif mode =="4":
                interactive_encryptor(outdir)
            elif mode == "5":
                interactive_crack_hash_cli(outdir)
            elif mode == "6":
                ok("Goodbye!")
                break
            else:
                warn("Invalid option, try again.")
    except KeyboardInterrupt:
        print()  # newline
        warn("Interrupted by user. Exiting.")

if __name__ == "__main__":
    main_loop()
    
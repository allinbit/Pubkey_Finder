import hashlib
import ecdsa
from binascii import unhexlify, hexlify
from multiprocessing import Process, Value, Lock, current_process

generator = ecdsa.SECP256k1.generator


def pubkey_to_hash160(pubkey_hex):
    pubkey_bytes = unhexlify(pubkey_hex)

    sha256 = hashlib.sha256(pubkey_bytes).digest()
    ripemd160 = hashlib.new('ripemd160')
    ripemd160.update(sha256)
    return ripemd160.hexdigest()


def compress_pubkey(pubkey_hex):
    pubkey_bytes = unhexlify(pubkey_hex)

    x = int(pubkey_bytes[1:33].hex(), 16)
    y = int(pubkey_bytes[33:].hex(), 16)

    prefix = b'\x02' if y % 2 == 0 else b'\x03'
    compressed_pubkey = prefix + x.to_bytes(32, 'big')

    return hexlify(compressed_pubkey).decode()


def point_addition(pubkey_hex, n=1):
    pubkey_bytes = unhexlify(pubkey_hex)
    curve = ecdsa.SECP256k1.curve

    x = int(pubkey_bytes[1:33].hex(), 16)
    y = int(pubkey_bytes[33:].hex(), 16)

    point = ecdsa.ellipticcurve.Point(curve, x, y)
    new_point = point + n * generator
    new_pubkey = b'\x04' + new_point.x().to_bytes(32, 'big') + new_point.y().to_bytes(32, 'big')

    return hexlify(new_pubkey).decode()


def worker(start_pubkey, target_hash160, attempts_per_process, total_attempts, lock, found_flag):
    current_pubkey = start_pubkey
    attempts = 0

    while attempts < attempts_per_process and not found_flag.value:
        compressed_pubkey = compress_pubkey(current_pubkey)
        current_hash160 = pubkey_to_hash160(compressed_pubkey)
        attempts += 1

        if current_hash160 == target_hash160:
            with lock:
                found_flag.value = True
                print(f"{current_process().name}: find matched publickey: {compressed_pubkey}")
                print(f"{current_process().name}: attempt numbers: {attempts}")
            break

        current_pubkey = point_addition(current_pubkey)
        #print(f"{current_process().name}: The {attempts}th attempt")
        #print(current_pubkey)

        #if attempts % 5000000000 == 0:
            #print(f"{current_process().name}: {attempts} attempts have been made...")

    with lock:
        total_attempts.value += attempts


def main():
    initial_pubkey = "041238c0766eaebea9ce4068a1f594d03b8ed4930d072d9c8b9164643e1516e6338a9db02dbb271359d6c979e2d1c3dc170946252dcc74022805cdb728c77b7805"
    target_hash160 = "739437bb3dd6d1983e66629c5f08c70e52769371"
    total_attempts_required = 2 ** 66

    num_processes = 16
    attempts_per_process = total_attempts_required // num_processes

    total_attempts = Value('i', 0)
    found_flag = Value('b', False)
    lock = Lock()

    start_pubkeys = [point_addition(initial_pubkey, n * attempts_per_process) for n in range(num_processes)]

    processes = []
    for i in range(num_processes):
        p = Process(target=worker, args=(start_pubkeys[i], target_hash160, attempts_per_process, total_attempts, lock, found_flag))
        p.start()
        processes.append(p)

    for p in processes:
        p.join()

    #print(f"total attempt numbers: {total_attempts.value}")


if __name__ == "__main__":
    main()

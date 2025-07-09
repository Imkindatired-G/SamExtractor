from datetime import datetime, UTC

# Convert Windows FILETIME to UNIX timestamp
def ft2dt(filetime):
    heptonion = int(1 / 10**-7) # Windows counts time in heptonions

    # Calculate difference between epochs
    windows_epoch = datetime.strptime('1601-01-01 00:00:00', '%Y-%m-%d %H:%M:%S')
    posix_epoch = datetime.strptime('1970-01-01 00:00:00', '%Y-%m-%d %H:%M:%S')

    epoch_diff = (posix_epoch - windows_epoch).total_seconds()

    # Calculate the difference between the two epochs in heptonions
    difference = epoch_diff * heptonion
    microseconds = (filetime - difference) // heptonion

    timestamp = None

    try:
        timestamp = datetime.fromtimestamp(microseconds, UTC)
    except OSError:
        print('❌ Error converting timestamp!')

    return timestamp

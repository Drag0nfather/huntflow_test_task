from argparse import ArgumentParser


def parse_arguments():
    parser = ArgumentParser()
    parser.add_argument(
        '-t',
        '--token',
        type=str,
        help='Huntflow Api token input'
    )
    parser.add_argument(
        '-p',
        '--path',
        type=str,
        help='Path to Excel file with applicants'
    )
    args = parser.parse_args()
    return args

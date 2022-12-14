import argparse
from scrapper import CancelAction, Scrapper

parser = argparse.ArgumentParser(
    prog="nf_cli.py",
    epilog="See repo: https://github.com/Emerson-MM-Filho/scrapper-nf-sc",
    description="Scrapper Nota Fiscal Eletrônica Florianópolis.",
    fromfile_prefix_chars="@"
)

parser.add_argument(
    "-cmc",
    "--codigomunicipal",
    type=int,
    help="Código municipal",
    dest="cmc",
    required=True,
)
parser.add_argument(
    "-e",
    "--email",
    type=str,
    help="Email",
    dest="email",
    required=True,
)
parser.add_argument(
    "-p",
    "--password",
    type=str,
    help="Senha",
    dest="password",
    required=True,
)
parser.add_argument(
    "-cl",
    "--clonelast",
    help="Should clone the last transmited fiscal note",
    dest="should_clone_last",
    action="store_true",
    default=False,
    required=False,
)
parser.add_argument(
    "-d",
    "--download",
    help="Should Download the last trasmited fiscal note",
    dest="should_download_last",
    action="store_true",
    default=False,
    required=False,
)
parser.add_argument(
    "-rc",
    "--requestconfirmation",
    help="Run the scrapper as normaly, but don't conclude the operation, user should confirm the operation manually",
    dest="request_confirmation",
    action="store_true",
    default=False,
    required=False,
)

args = parser.parse_args()

def main():
    scrapper = Scrapper(args.cmc, args.email, args.password)
    scrapper.login()

    if args.should_clone_last:
        try:
            scrapper.clone_last_consult_result(args.request_confirmation)
        except CancelAction:
            raise

    if args.should_download_last:
        scrapper.download_last_consult_result()

if __name__ == "__main__":
    try:
        main()
    except CancelAction as exc:
        print(exc)

import sys
import json
from pathlib import Path

from gemini_service import extract_bill_data


def main():

    if len(sys.argv) != 2:
        print(
            "Usage:\n"
            "python local_test.py test_data/sample_bill.pdf"
        )
        sys.exit(1)

    pdf_path = Path(sys.argv[1])

    print("=" * 60)
    print("ENERGY AUDITOR - LOCAL BILL EXTRACTION TEST")
    print("=" * 60)

    try:

        bill = extract_bill_data(str(pdf_path))

        output = bill.model_dump()

        print("\n")
        print("=" * 60)
        print("EXTRACTED BILL DATA")
        print("=" * 60)

        print(
            json.dumps(
                output,
                indent=4,
                ensure_ascii=False
            )
        )

        output_dir = Path("output")
        output_dir.mkdir(exist_ok=True)

        output_file = (
            output_dir / "extracted_bill.json"
        )

        with open(
            output_file,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                output,
                file,
                indent=4,
                ensure_ascii=False
            )

        print("\n")
        print("=" * 60)
        print(f"JSON saved to: {output_file}")
        print("=" * 60)

    except Exception as error:

        print("\n")
        print("=" * 60)
        print("ERROR")
        print("=" * 60)

        print(type(error).__name__)
        print(str(error))

        sys.exit(1)


if __name__ == "__main__":
    main()
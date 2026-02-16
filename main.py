"""
スキャンフォルダ整理ツール - メインCLI
"""
import argparse
import sys
from pathlib import Path

from document_processor.processors.financial_processor import FinancialProcessor
from document_processor.processors.vehicle_processor import VehicleProcessor
from document_processor.processors.employee_processor import EmployeeProcessor


def main():
    parser = argparse.ArgumentParser(
        description="スキャンフォルダから各種台帳を自動生成するツール"
    )
    parser.add_argument(
        "--company",
        "-c",
        required=True,
        help="企業フォルダパス (例: A918_株式会社野木工業)",
    )
    parser.add_argument(
        "--only",
        "-o",
        choices=["financial", "vehicles", "employees", "all"],
        default="all",
        help="処理する台帳の種類を指定 (デフォルト: all)",
    )

    args = parser.parse_args()

    # 企業フォルダの存在確認
    company_path = Path(args.company)
    if not company_path.exists():
        print(f"エラー: 企業フォルダが見つかりません: {args.company}")
        sys.exit(1)

    company_name = company_path.name
    print(f"\n{'='*60}")
    print(f"スキャンフォルダ整理ツール")
    print(f"対象企業: {company_name}")
    print(f"{'='*60}\n")

    results = {}

    # 財務概要処理
    if args.only in ["financial", "all"]:
        try:
            processor = FinancialProcessor()
            result = processor.process_company(str(company_path))
            results["財務概要"] = result
        except Exception as e:
            print(f"\n[NG] 財務概要処理エラー: {e}")
            results["財務概要"] = None

    # 車両台帳処理
    if args.only in ["vehicles", "all"]:
        try:
            processor = VehicleProcessor()
            result = processor.process_company(str(company_path))
            results["車両台帳"] = result
        except Exception as e:
            print(f"\n[NG] 車両台帳処理エラー: {e}")
            results["車両台帳"] = None

    # 従業員台帳処理
    if args.only in ["employees", "all"]:
        try:
            processor = EmployeeProcessor()
            result = processor.process_company(str(company_path))
            results["従業員台帳"] = result
        except Exception as e:
            print(f"\n[NG] 従業員台帳処理エラー: {e}")
            results["従業員台帳"] = None

    # 結果サマリー
    print(f"\n{'='*60}")
    print(f"処理完了サマリー")
    print(f"{'='*60}")
    for name, path in results.items():
        if path:
            print(f"[OK] {name}: {path}")
        else:
            print(f"[NG] {name}: 生成失敗")
    print()


if __name__ == "__main__":
    main()

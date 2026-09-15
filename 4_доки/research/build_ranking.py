#!/usr/bin/env python3
"""Aggregate trump_months_raw.json into a monthly ranking + Ukrainian report."""
import json
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).parent
RAW = HERE / "trump_months_raw.json"
MD_OUT = HERE / "trump_months_ranking.md"

SCORE_WEIGHTS = {"pants-fire": 3, "false": 2, "mostly-false": 1}
FALSE_SET = {"pants-fire", "false", "mostly-false"}

RULING_LABEL = {
    "pants-fire": "pants-fire",
    "false": "false",
    "mostly-false": "mostly-false",
    "half-true": "half-true",
    "mostly-true": "mostly-true",
    "true": "true",
    "full-flop": "full-flop",
    "half-flip": "half-flip",
    "no-flip": "no-flip",
}

MONTHS_UA = {
    1: "січень", 2: "лютий", 3: "березень", 4: "квітень", 5: "травень", 6: "червень",
    7: "липень", 8: "серпень", 9: "вересень", 10: "жовтень", 11: "листопад", 12: "грудень",
}


def month_key(date_str: str) -> str:
    return date_str[:7]  # YYYY-MM


def main():
    items = json.loads(RAW.read_text())

    by_month = defaultdict(list)
    for it in items:
        by_month[month_key(it["date"])].append(it)

    rows = []
    for mk, its in by_month.items():
        counts = defaultdict(int)
        for it in its:
            counts[it["ruling"]] += 1
        total = len(its)
        score = sum(SCORE_WEIGHTS.get(it["ruling"], 0) for it in its)
        false_n = sum(1 for it in its if it["ruling"] in FALSE_SET)
        share_false = false_n / total if total else 0
        y, m = mk.split("-")
        rows.append({
            "month": mk,
            "label": f"{MONTHS_UA[int(m)]} {y}",
            "score": score,
            "pants_fire": counts.get("pants-fire", 0),
            "false": counts.get("false", 0),
            "mostly_false": counts.get("mostly-false", 0),
            "total": total,
            "share_false": share_false,
            "low_confidence": total < 5,
            "items": its,
        })

    rows.sort(key=lambda r: (-r["score"], -r["share_false"]))
    for i, r in enumerate(rows, 1):
        r["rank"] = i

    # ---- Markdown (Ukrainian) ----
    lines = []
    lines.append("# Рейтинг місяців другого терміну Трампа за \"дурнею\" (PolitiFact)")
    lines.append("")
    lines.append(
        "**Метод (коротко):** PolitiFact перевіряє не всі заяви Трампа, а вибірку "
        "(ту, що зацікавила редакцію) — тому це відносний рейтинг \"скільки маячні "
        "впіймали фактчекери\", а не повний облік усієї брехні за місяць. "
        "Дані: https://www.politifact.com/factchecks/list/?speaker=donald-trump, "
        "статті з датою заяви від 2025-01-20 до 2026-08-10 (пізніших фактчеків на "
        "момент збору ще не опубліковано)."
    )
    lines.append("")
    lines.append(
        "Скор = pants-fire×3 + false×2 + mostly-false×1. `% false` = "
        "(pants-fire+false+mostly-false)/усі оцінені за місяць. "
        "Місяці з менш ніж 5 оціненими заявами позначені як low-confidence "
        "(мала вибірка, рейтинг ненадійний)."
    )
    lines.append("")
    lines.append("## Рейтингова таблиця")
    lines.append("")
    lines.append("| # | Місяць | Скор | pants-fire | false | mostly-false | Всього оцінено | % false | Впевненість |")
    lines.append("|---|---|---|---|---|---|---|---|---|")
    for r in rows:
        conf = "низька (n<5)" if r["low_confidence"] else "норм"
        lines.append(
            f"| {r['rank']} | {r['label']} | {r['score']} | {r['pants_fire']} | "
            f"{r['false']} | {r['mostly_false']} | {r['total']} | "
            f"{r['share_false']*100:.0f}% | {conf} |"
        )
    lines.append("")
    lines.append(
        f"*Разом зібрано {len(items)} перевірених заяв Трампа за період другого "
        f"терміну (з {len(rows)} місяців, що мають хоч одну оцінену заяву)."
    )
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## Перли по місяцях (у порядку рейтингу)")
    lines.append("")
    lines.append(
        "Для кожного місяця — топ-5 кандидатів на відео: спочатку pants-fire, "
        "потім false, перевага коротким/абсурдним/вірусним заявам."
    )
    lines.append("")

    for r in rows:
        lines.append(f"### {r['rank']}. {r['label']} — скор {r['score']}, {r['total']} оцінено"
                      + (" (low-confidence)" if r["low_confidence"] else ""))
        lines.append("")

        def sort_key(it):
            order = {"pants-fire": 0, "false": 1, "mostly-false": 2}
            rank = order.get(it["ruling"], 3)
            return (rank, len(it["statement"]))

        pearls = sorted(r["items"], key=sort_key)[:5]
        if not pearls:
            lines.append("_немає оцінених заяв._")
        for it in pearls:
            lines.append(f"- **{it['date']}** [{RULING_LABEL.get(it['ruling'], it['ruling'])}]")
            lines.append(f"  - EN: \"{it['statement']}\"")
            lines.append(f"  - UA: _(переклад-заготовка, перевірити перед використанням)_")
            lines.append(f"  - {it['url']}")
        lines.append("")

    MD_OUT.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote {MD_OUT}")
    print(f"\nTop 20 rows:\n")
    print("rank | month | score | pf | false | mf | total | %false | conf")
    for r in rows[:20]:
        conf = "LOW" if r["low_confidence"] else "ok"
        print(f"{r['rank']:2d} | {r['label']:14s} | {r['score']:3d} | {r['pants_fire']:2d} | "
              f"{r['false']:2d} | {r['mostly_false']:2d} | {r['total']:2d} | "
              f"{r['share_false']*100:5.1f}% | {conf}")


if __name__ == "__main__":
    main()

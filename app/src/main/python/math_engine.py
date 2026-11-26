"""
Safe, deterministic AST-based Math, Statistics, Unit Conversion, Horticulture,
and Computer Science calculator engine. Strictly NO raw eval().
"""

from __future__ import annotations

import ast
import ipaddress
import math
import operator
import re
import statistics
from typing import Any, Callable, Dict, List, Optional, Tuple

import numpy as np


# --- Safe AST Evaluator ---

_BIN_OPS: Dict[type, Callable[[float, float], float]] = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
}

_UNARY_OPS: Dict[type, Callable[[float], float]] = {
    ast.UAdd: operator.pos,
    ast.USub: operator.neg,
}

_SAFE_FUNCS: Dict[str, Callable[..., float]] = {
    "sqrt": math.sqrt,
    "cbrt": lambda x: math.copysign(abs(x) ** (1.0 / 3.0), x),
    "abs": abs,
    "round": round,
    "floor": math.floor,
    "ceil": math.ceil,
    "sin": math.sin,
    "cos": math.cos,
    "tan": math.tan,
    "sind": lambda x: math.sin(math.radians(x)),
    "cosd": lambda x: math.cos(math.radians(x)),
    "tand": lambda x: math.tan(math.radians(x)),
    "asin": math.asin,
    "acos": math.acos,
    "atan": math.atan,
    "sinh": math.sinh,
    "cosh": math.cosh,
    "tanh": math.tanh,
    "log": math.log10,
    "log10": math.log10,
    "log2": math.log2,
    "ln": math.log,
    "exp": math.exp,
    "factorial": lambda n: float(math.factorial(int(n))),
    "fact": lambda n: float(math.factorial(int(n))),
    "gcd": lambda a, b: float(math.gcd(int(a), int(b))),
    "lcm": lambda a, b: float(math.lcm(int(a), int(b))),
    "pow": math.pow,
    "min": min,
    "max": max,
    "deg": math.degrees,
    "degrees": math.degrees,
    "rad": math.radians,
    "radians": math.radians,
    "percent": lambda part, whole: (part / whole) * 100.0,
}

_SAFE_CONSTS: Dict[str, float] = {
    "pi": math.pi,
    "e": math.e,
    "tau": math.tau,
}


def _eval_ast_node(node: ast.AST) -> float:
    if isinstance(node, ast.Expression):
        return _eval_ast_node(node.body)
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
        if isinstance(node.value, bool):
            raise ValueError("Boolean literals are not numeric.")
        return float(node.value)
    if isinstance(node, ast.Name):
        ident = node.id.lower()
        if ident in _SAFE_CONSTS:
            return _SAFE_CONSTS[ident]
        raise ValueError(f"Unknown symbol: {node.id}")
    if isinstance(node, ast.BinOp):
        op_type = type(node.op)
        if op_type not in _BIN_OPS:
            raise ValueError("Unsupported binary operator.")
        left = _eval_ast_node(node.left)
        right = _eval_ast_node(node.right)
        if op_type is ast.Pow and abs(right) > 1000:
            raise ValueError("Exponent magnitude too large.")
        return float(_BIN_OPS[op_type](left, right))
    if isinstance(node, ast.UnaryOp):
        op_type = type(node.op)
        if op_type not in _UNARY_OPS:
            raise ValueError("Unsupported unary operator.")
        return float(_UNARY_OPS[op_type](_eval_ast_node(node.operand)))
    if isinstance(node, ast.Call):
        if not isinstance(node.func, ast.Name):
            raise ValueError("Unsupported function call.")
        func_name = node.func.id.lower()
        if func_name not in _SAFE_FUNCS:
            raise ValueError(f"Unknown function: {node.func.id}")
        if node.keywords:
            raise ValueError("Keyword arguments are not supported.")
        args = [_eval_ast_node(arg) for arg in node.args]
        return float(_SAFE_FUNCS[func_name](*args))
    raise ValueError("Unsupported expression syntax.")


def safe_eval_math(expr: str) -> float:
    cleaned = expr.strip()
    # Replace unicode operators & power caret
    cleaned = cleaned.replace("×", "*").replace("÷", "/").replace("−", "-")
    cleaned = cleaned.replace("√", "sqrt")
    # Convert n! to factorial(n)
    cleaned = re.sub(r"(\d+)\s*!", r"factorial(\1)", cleaned)
    # Convert sin(30 deg) or sin(30°) to sind(30)
    cleaned = re.sub(
        r"\b(sin|cos|tan)\s*\(\s*([^()]+?)\s*(?:deg|degrees|°)\s*\)",
        r"\1d(\2)",
        cleaned,
        flags=re.IGNORECASE,
    )
    cleaned = cleaned.replace("^", "**")
    # Implicit multiplication like 2pi or 3(4+5)
    cleaned = re.sub(r"(\d)\s*(pi|e|tau)\b", r"\1*\2", cleaned, flags=re.IGNORECASE)
    cleaned = re.sub(r"(\d)\s*\(", r"\1*(", cleaned)
    cleaned = re.sub(r"\)\s*(\d)", r")*\1", cleaned)
    tree = ast.parse(cleaned, mode="eval")
    return _eval_ast_node(tree)


def _fmt_num(val: float) -> str:
    if math.isnan(val) or math.isinf(val):
        return str(val)
    if abs(val - round(val)) < 1e-10 and abs(val) < 1e15:
        return str(int(round(val)))
    return f"{val:.6g}" if abs(val) >= 1e6 or (0 < abs(val) < 1e-4) else f"{val:.4f}".rstrip("0").rstrip(".")


# --- Big-O Reference Table ---

_BIG_O_DB: Dict[str, Dict[str, str]] = {
    "binary search": {
        "name": "Binary Search",
        "best": "O(1)",
        "average": "O(log n)",
        "worst": "O(log n)",
        "space": "O(1) iterative / O(log n) recursive",
        "note": "Requires a sorted array or monotonic search space.",
    },
    "linear search": {
        "name": "Linear Search",
        "best": "O(1)",
        "average": "O(n)",
        "worst": "O(n)",
        "space": "O(1)",
        "note": "Works on unsorted lists.",
    },
    "quicksort": {
        "name": "Quick Sort",
        "best": "O(n log n)",
        "average": "O(n log n)",
        "worst": "O(n²)",
        "space": "O(log n) stack",
        "note": "In-place divide-and-conquer; worst case avoided with randomized or median-of-three pivot.",
    },
    "merge sort": {
        "name": "Merge Sort",
        "best": "O(n log n)",
        "average": "O(n log n)",
        "worst": "O(n log n)",
        "space": "O(n)",
        "note": "Stable sorting algorithm ideal for linked lists and external sorting.",
    },
    "heap sort": {
        "name": "Heap Sort",
        "best": "O(n log n)",
        "average": "O(n log n)",
        "worst": "O(n log n)",
        "space": "O(1)",
        "note": "In-place, not stable.",
    },
    "bubble sort": {
        "name": "Bubble Sort",
        "best": "O(n)",
        "average": "O(n²)",
        "worst": "O(n²)",
        "space": "O(1)",
        "note": "Educational only; slow for large datasets.",
    },
    "insertion sort": {
        "name": "Insertion Sort",
        "best": "O(n)",
        "average": "O(n²)",
        "worst": "O(n²)",
        "space": "O(1)",
        "note": "Very fast for small or nearly sorted arrays (used inside Timsort).",
    },
    "hash table": {
        "name": "Hash Table (Lookup / Insert / Delete)",
        "best": "O(1)",
        "average": "O(1)",
        "worst": "O(n)",
        "space": "O(n)",
        "note": "O(1) amortized with good hash function and load factor < 0.75.",
    },
    "bst": {
        "name": "Binary Search Tree (Search / Insert)",
        "best": "O(log n)",
        "average": "O(log n)",
        "worst": "O(n) skewed",
        "space": "O(n)",
        "note": "Self-balancing trees (AVL, Red-Black) guarantee O(log n) worst case.",
    },
    "bfs": {
        "name": "Breadth-First Search (BFS)",
        "best": "O(V + E)",
        "average": "O(V + E)",
        "worst": "O(V + E)",
        "space": "O(V)",
        "note": "Finds shortest path in unweighted graphs using a queue.",
    },
    "dfs": {
        "name": "Depth-First Search (DFS)",
        "best": "O(V + E)",
        "average": "O(V + E)",
        "worst": "O(V + E)",
        "space": "O(V)",
        "note": "Uses recursion/stack; useful for topological sort and cycle detection.",
    },
    "dijkstra": {
        "name": "Dijkstra's Shortest Path (Min-Heap)",
        "best": "O((V + E) log V)",
        "average": "O((V + E) log V)",
        "worst": "O((V + E) log V)",
        "space": "O(V)",
        "note": "Requires non-negative edge weights.",
    },
}


# --- Unit Conversion Tables ---

_LENGTH_TO_M: Dict[str, float] = {
    "mm": 0.001, "millimeter": 0.001, "millimeters": 0.001,
    "cm": 0.01, "centimeter": 0.01, "centimeters": 0.01,
    "m": 1.0, "meter": 1.0, "meters": 1.0,
    "km": 1000.0, "kilometer": 1000.0, "kilometers": 1000.0,
    "in": 0.0254, "inch": 0.0254, "inches": 0.0254,
    "ft": 0.3048, "foot": 0.3048, "feet": 0.3048,
    "yd": 0.9144, "yard": 0.9144, "yards": 0.9144,
    "mi": 1609.344, "mile": 1609.344, "miles": 1609.344,
}

_AREA_TO_M2: Dict[str, float] = {
    "m2": 1.0, "sqm": 1.0, "m^2": 1.0,
    "ha": 10000.0, "hectare": 10000.0, "hectares": 10000.0,
    "timad": 2500.0, "timads": 2500.0,  # Ethiopian traditional unit: 1 ha = 4 timad
    "acre": 4046.8564224, "acres": 4046.8564224,
    "km2": 1_000_000.0, "sqkm": 1_000_000.0, "km^2": 1_000_000.0,
    "cm2": 0.0001, "ft2": 0.09290304, "sqft": 0.09290304,
}

_MASS_TO_KG: Dict[str, float] = {
    "mg": 1e-6, "g": 0.001, "gram": 0.001, "grams": 0.001,
    "kg": 1.0, "kilogram": 1.0, "kilograms": 1.0,
    "quintal": 100.0, "quintals": 100.0, "qt": 100.0,
    "ton": 1000.0, "tons": 1000.0, "tonne": 1000.0, "tonnes": 1000.0, "t": 1000.0,
    "lb": 0.45359237, "lbs": 0.45359237, "pound": 0.45359237, "pounds": 0.45359237,
    "oz": 0.028349523125, "ounce": 0.028349523125,
}

_DATA_TO_BITS: Dict[str, float] = {
    "bit": 1.0, "bits": 1.0, "b_bit": 1.0,
    "byte": 8.0, "bytes": 8.0, "b": 8.0,
    "kb": 8.0 * 1000.0, "mb": 8.0 * 1000.0**2, "gb": 8.0 * 1000.0**3, "tb": 8.0 * 1000.0**4,
    "kib": 8.0 * 1024.0, "mib": 8.0 * 1024.0**2, "gib": 8.0 * 1024.0**3, "tib": 8.0 * 1024.0**4,
}


def _result(
    answer: str,
    category: str = "Math",
    steps: str = "",
    tag: str = "Deterministic Engine",
) -> Dict[str, Any]:
    return {
        "matched": True,
        "answer": answer,
        "category": category,
        "confidence": 1.0,
        "route": "math_engine",
        "steps": steps,
        "tag": tag,
    }


def _extract_area_m2(text: str) -> Optional[Tuple[float, str]]:
    m = re.search(
        r"(\d+(?:\.\d+)?)\s*(ha|hectares?|timads?|acres?|m2|sqm|m\^2|km2)\b",
        text,
        re.IGNORECASE,
    )
    if not m:
        return None
    val = float(m.group(1))
    unit = m.group(2).lower()
    factor = _AREA_TO_M2.get(unit)
    if factor is None:
        return None
    return val * factor, f"{_fmt_num(val)} {unit}"


# --- Specific Domain Calculators ---

def _try_horticulture_calculators(q: str) -> Optional[Dict[str, Any]]:
    ql = q.lower()

    # 1. Fertilizer Rate & NPK Dosage Calculator
    # Examples:
    # "fertilizer 100 kg/ha 500 m2"
    # "npk 46-0-0 rate 150 kg/ha area 0.25 ha"
    # "urea 100 kg/ha 2 timad"
    if any(k in ql for k in ("fertilizer", "fertiliser", "npk", "urea", "dap", "nps")):
        rate_m = re.search(r"(\d+(?:\.\d+)?)\s*kg\s*/?\s*ha", ql)
        area_info = _extract_area_m2(ql)
        npk_m = re.search(r"(\d+(?:\.\d+)?)\s*[-:]\s*(\d+(?:\.\d+)?)\s*[-:]\s*(\d+(?:\.\d+)?)", ql)

        # Smart defaults for common Ethiopian fertilizers if grade omitted
        if not npk_m:
            if "urea" in ql:
                n_pct, p_pct, k_pct = 46.0, 0.0, 0.0
                grade_label = "Urea (46-0-0)"
            elif "dap" in ql:
                n_pct, p_pct, k_pct = 18.0, 46.0, 0.0
                grade_label = "DAP (18-46-0)"
            elif "nps" in ql:
                n_pct, p_pct, k_pct = 19.0, 38.0, 0.0
                grade_label = "NPS (19-38-0 +7S)"
            else:
                n_pct, p_pct, k_pct = 0.0, 0.0, 0.0
                grade_label = "Unspecified Grade"
        else:
            n_pct, p_pct, k_pct = float(npk_m.group(1)), float(npk_m.group(2)), float(npk_m.group(3))
            grade_label = f"NPK ({_fmt_num(n_pct)}-{_fmt_num(p_pct)}-{_fmt_num(k_pct)})"

        if rate_m and area_info:
            rate_kg_ha = float(rate_m.group(1))
            area_m2, area_label = area_info
            area_ha = area_m2 / 10000.0
            total_kg = rate_kg_ha * area_ha
            total_g = total_kg * 1000.0

            lines = [
                f"**Fertilizer Dosage Result ({grade_label})**",
                f"• Application Rate: {_fmt_num(rate_kg_ha)} kg/ha",
                f"• Plot Area: {area_label} ({_fmt_num(area_m2)} m² = {_fmt_num(area_ha)} ha)",
                f"• **Required Fertilizer: {_fmt_num(total_kg)} kg ({_fmt_num(total_g)} g)**",
            ]
            if n_pct + p_pct + k_pct > 0:
                n_kg = total_kg * (n_pct / 100.0)
                p_kg = total_kg * (p_pct / 100.0)
                k_kg = total_kg * (k_pct / 100.0)
                lines.append(
                    f"• Elemental Nutrients Supplied: N = {_fmt_num(n_kg)} kg, P₂O₅ = {_fmt_num(p_kg)} kg, K₂O = {_fmt_num(k_kg)} kg"
                )
            steps = f"Dose = Rate ({rate_kg_ha} kg/ha) × (Area {area_m2} m² / 10,000 m²/ha) = {_fmt_num(total_kg)} kg"
            return _result("\n".join(lines), category="Horticulture", steps=steps, tag="Horticulture Calc")

    # 2. Plant Population / Spacing Calculator
    # Examples: "spacing 0.75 x 0.30 area 1 ha", "population row 0.8 plant 0.4 area 2500 m2"
    if any(k in ql for k in ("spacing", "population", "plants per", "plant density")):
        pair_m = re.search(r"(\d+(?:\.\d+)?)\s*(?:m|cm)?\s*[x×by]+\s*(\d+(?:\.\d+)?)\s*(cm|m)?", ql)
        row_m = re.search(r"row\s*(?:spacing)?\s*[:=]?\s*(\d+(?:\.\d+)?)\s*(cm|m)?", ql)
        plant_m = re.search(r"plant\s*(?:spacing)?\s*[:=]?\s*(\d+(?:\.\d+)?)\s*(cm|m)?", ql)

        row_m_val: Optional[float] = None
        plant_m_val: Optional[float] = None

        if pair_m:
            r_raw, p_raw = float(pair_m.group(1)), float(pair_m.group(2))
            unit = (pair_m.group(3) or "m").lower()
            div = 100.0 if unit == "cm" else 1.0
            row_m_val, plant_m_val = r_raw / div, p_raw / div
        elif row_m and plant_m:
            r_raw = float(row_m.group(1))
            p_raw = float(plant_m.group(1))
            row_m_val = r_raw / (100.0 if (row_m.group(2) or "m").lower() == "cm" else 1.0)
            plant_m_val = p_raw / (100.0 if (plant_m.group(2) or "m").lower() == "cm" else 1.0)

        if row_m_val and plant_m_val and row_m_val > 0 and plant_m_val > 0:
            area_info = _extract_area_m2(ql)
            area_m2, area_label = area_info if area_info else (10000.0, "1 ha (default)")
            plants = area_m2 / (row_m_val * plant_m_val)
            plants_per_ha = 10000.0 / (row_m_val * plant_m_val)
            with_gap = plants * 1.10
            answer = (
                f"**Plant Population Calculation**\n"
                f"• Spacing: {_fmt_num(row_m_val)} m (row) × {_fmt_num(plant_m_val)} m (intra-row)\n"
                f"• Target Area: {area_label} ({_fmt_num(area_m2)} m²)\n"
                f"• **Estimated Plant Population: {int(round(plants)):,} plants**\n"
                f"• Equivalent Density: {int(round(plants_per_ha)):,} plants/ha\n"
                f"• Nursery Allowance (+10% gap filling): {int(round(with_gap)):,} seedlings"
            )
            steps = f"Population = {area_m2} m² / ({row_m_val} m × {plant_m_val} m) = {int(round(plants)):,}"
            return _result(answer, category="Horticulture", steps=steps, tag="Horticulture Calc")

    # 3. Irrigation Water Requirement Calculator
    # Example: "irrigation eto 5 kc 1.15 area 1 ha eff 0.7"
    if any(k in ql for k in ("irrigation", "etc", "eto", "water requirement")):
        eto_m = re.search(r"eto\s*[:=]?\s*(\d+(?:\.\d+)?)", ql)
        kc_m = re.search(r"kc\s*[:=]?\s*(\d+(?:\.\d+)?)", ql)
        eff_m = re.search(r"eff(?:iciency)?\s*[:=]?\s*(\d+(?:\.\d+)?)", ql)
        if eto_m and kc_m:
            eto = float(eto_m.group(1))
            kc = float(kc_m.group(1))
            eff = float(eff_m.group(1)) if eff_m else 0.75
            if eff > 1.0:
                eff = eff / 100.0
            area_info = _extract_area_m2(ql)
            area_m2, area_label = area_info if area_info else (10000.0, "1 ha (default)")
            etc_mm = eto * kc
            gross_mm = etc_mm / max(eff, 0.05)
            net_liters = etc_mm * area_m2  # 1 mm over 1 m2 = 1 liter
            gross_liters = gross_mm * area_m2
            gross_m3 = gross_liters / 1000.0
            answer = (
                f"**Crop Irrigation Water Requirement**\n"
                f"• Crop Evapotranspiration (ETc = ETo × Kc): **{_fmt_num(etc_mm)} mm/day**\n"
                f"• Application Efficiency: {_fmt_num(eff * 100)}%\n"
                f"• Gross Irrigation Depth: **{_fmt_num(gross_mm)} mm/day**\n"
                f"• Target Area: {area_label}\n"
                f"• **Daily Gross Volume: {_fmt_num(gross_m3)} m³/day ({int(round(gross_liters)):,} L/day)**\n"
                f"• Daily Net Volume: {_fmt_num(net_liters / 1000.0)} m³/day"
            )
            steps = f"ETc = {eto} × {kc} = {_fmt_num(etc_mm)} mm; Gross = {_fmt_num(etc_mm)} / {eff} = {_fmt_num(gross_mm)} mm"
            return _result(answer, category="Horticulture", steps=steps, tag="Irrigation Calc")

    # 4. Postharvest Moisture & Yield Loss Percentage
    # Example: "loss initial 1200 final 1020" or "moisture wet 500 dry 425"
    if any(k in ql for k in ("moisture", "yield loss", "weight loss", "postharvest loss", "loss initial")):
        nums = [float(x) for x in re.findall(r"\d+(?:\.\d+)?", ql)]
        if len(nums) >= 2:
            initial_w, final_w = nums[0], nums[1]
            if initial_w > 0 and final_w <= initial_w:
                diff = initial_w - final_w
                wet_pct = (diff / initial_w) * 100.0
                if "moisture" in ql and final_w > 0:
                    dry_pct = (diff / final_w) * 100.0
                    answer = (
                        f"**Postharvest Moisture Content**\n"
                        f"• Wet Sample Mass: {_fmt_num(initial_w)} | Dry Mass: {_fmt_num(final_w)}\n"
                        f"• Moisture Lost: {_fmt_num(diff)}\n"
                        f"• **Moisture Content (Wet Basis): {_fmt_num(wet_pct)}%**\n"
                        f"• Moisture Content (Dry Basis): {_fmt_num(dry_pct)}%\n"
                        f"• *Coffee parchment safe storage target: 10.5%–11.5% wet basis.*"
                    )
                    steps = f"MC(wb) = ({initial_w} - {final_w}) / {initial_w} × 100 = {_fmt_num(wet_pct)}%"
                    return _result(answer, category="Horticulture", steps=steps, tag="Postharvest Calc")
                else:
                    answer = (
                        f"**Postharvest Yield / Weight Loss**\n"
                        f"• Initial Mass: {_fmt_num(initial_w)} | Final Mass: {_fmt_num(final_w)}\n"
                        f"• Total Loss: {_fmt_num(diff)}\n"
                        f"• **Percentage Loss: {_fmt_num(wet_pct)}%**"
                    )
                    steps = f"Loss % = ({initial_w} - {final_w}) / {initial_w} × 100 = {_fmt_num(wet_pct)}%"
                    return _result(answer, category="Horticulture", steps=steps, tag="Postharvest Calc")

    # 5. Horticulture Chemical / Foliar Spray Dilution Calculator (C1 * V1 = C2 * V2)
    # Example: "dilution c1 50 c2 0.5 v2 20"
    if "dilution" in ql or ("c1" in ql and "c2" in ql):
        c1_m = re.search(r"c1\s*[:=]?\s*(\d+(?:\.\d+)?)", ql)
        c2_m = re.search(r"c2\s*[:=]?\s*(\d+(?:\.\d+)?)", ql)
        v2_m = re.search(r"v2\s*[:=]?\s*(\d+(?:\.\d+)?)", ql)
        if c1_m and c2_m and v2_m:
            c1, c2, v2 = float(c1_m.group(1)), float(c2_m.group(1)), float(v2_m.group(1))
            if c1 > 0:
                v1 = (c2 * v2) / c1
                water = max(0.0, v2 - v1)
                answer = (
                    f"**Spray Dilution Calculation (`C₁V₁ = C₂V₂`)**\n"
                    f"• Stock Concentration (C₁): `{_fmt_num(c1)}` | Target (C₂): `{_fmt_num(c2)}`\n"
                    f"• Final Sprayer Volume (V₂): `{_fmt_num(v2)} L`\n"
                    f"• **Stock Chemical Needed (V₁): `{_fmt_num(v1)} L` (`{_fmt_num(v1 * 1000)} mL`)**\n"
                    f"• Clean Water to Add: `{_fmt_num(water)} L`"
                )
                steps = f"V₁ = ({c2} × {v2}) / {c1} = {_fmt_num(v1)} L"
                return _result(answer, category="Horticulture", steps=steps, tag="Spray Dilution")

    # 6. Agricultural ROI / Gross Margin Calculator
    # Example: "roi cost 5000 revenue 8500"
    if "roi" in ql or ("cost" in ql and "revenue" in ql):
        cost_m = re.search(r"cost\s*[:=]?\s*(\d+(?:\.\d+)?)", ql)
        rev_m = re.search(r"(?:revenue|income|sales)\s*[:=]?\s*(\d+(?:\.\d+)?)", ql)
        if cost_m and rev_m:
            cost, rev = float(cost_m.group(1)), float(rev_m.group(1))
            if cost > 0:
                profit = rev - cost
                roi_pct = (profit / cost) * 100.0
                bcr = rev / cost
                answer = (
                    f"**Farm Profitability & ROI**\n"
                    f"• Total Input Cost: `{_fmt_num(cost)}` | Gross Revenue: `{_fmt_num(rev)}`\n"
                    f"• Net Profit: **`{_fmt_num(profit)}`**\n"
                    f"• **Return on Investment (ROI): `{_fmt_num(roi_pct)}%`**\n"
                    f"• Benefit-Cost Ratio (BCR): `{_fmt_num(bcr)}`"
                )
                steps = f"ROI = (({rev} - {cost}) / {cost}) × 100 = {_fmt_num(roi_pct)}%"
                return _result(answer, category="Horticulture", steps=steps, tag="Farm Economics")

    return None


def _try_cs_calculators(q: str) -> Optional[Dict[str, Any]]:
    ql = q.lower().strip()

    # 1. IPv4 Subnet Mask & Host Count Calculator
    cidr_m = re.search(r"(\d{1,3}(?:\.\d{1,3}){3})\s*/\s*(\d{1,2})", ql)
    prefix_only_m = re.search(r"(?:subnet|cidr|mask)\s*/?(\d{1,2})\b", ql)
    if cidr_m or prefix_only_m:
        try:
            if cidr_m:
                ip_str, prefix = cidr_m.group(1), int(cidr_m.group(2))
                net = ipaddress.IPv4Network(f"{ip_str}/{prefix}", strict=False)
            else:
                prefix = int(prefix_only_m.group(1))
                net = ipaddress.IPv4Network(f"192.168.1.0/{prefix}", strict=False)

            total_addrs = net.num_addresses
            usable = max(0, total_addrs - 2) if prefix < 31 else (2 if prefix == 31 else 1)
            hosts = list(net.hosts()) if total_addrs <= 65536 else []
            first_host = str(hosts[0]) if hosts else str(net.network_address + 1)
            last_host = str(hosts[-1]) if hosts else str(net.broadcast_address - 1)
            if prefix >= 31:
                first_host = str(net.network_address)
                last_host = str(net.broadcast_address)

            answer = (
                f"**IPv4 Subnet Analysis (`/{prefix}`)**\n"
                f"• Network Address: `{net.network_address}/{prefix}`\n"
                f"• Subnet Mask: `{net.netmask}`\n"
                f"• Wildcard Mask: `{net.hostmask}`\n"
                f"• Broadcast Address: `{net.broadcast_address}`\n"
                f"• Usable Host Range: `{first_host}` – `{last_host}`\n"
                f"• Total IPs: `{total_addrs:,}` | **Usable Hosts: `{usable:,}`**"
            )
            steps = f"Usable hosts = 2^(32 - {prefix}) - 2 = 2^{32 - prefix} - 2 = {usable:,}"
            return _result(answer, category="Computer Science", steps=steps, tag="Networking Calc")
        except ValueError:
            pass

    # 2. Binary / Decimal / Hexadecimal / Octal Conversions
    bin_lit = re.search(r"\b0b([01]+)\b", ql)
    hex_lit = re.search(r"\b0x([0-9a-f]+)\b", ql)
    base_cmd = re.match(
        r"^(?:to\s+)?(bin|binary|hex|hexadecimal|oct|octal|dec|decimal)\s+([0-9a-fx]+)$",
        ql,
    )
    convert_phrase = re.search(
        r"(?:convert\s+)?([0-9a-fx]+)\s+(?:to|in)\s+(bin|binary|hex|hexadecimal|oct|octal|dec|decimal)\b",
        ql,
    )

    parsed_int: Optional[int] = None
    if bin_lit and ("to" in ql or "dec" in ql or "hex" in ql or len(ql.split()) <= 3):
        parsed_int = int(bin_lit.group(1), 2)
    elif hex_lit and ("to" in ql or "dec" in ql or "bin" in ql or len(ql.split()) <= 3):
        parsed_int = int(hex_lit.group(1), 16)
    elif base_cmd:
        mode, val_str = base_cmd.group(1), base_cmd.group(2)
        if val_str.startswith("0x"):
            parsed_int = int(val_str, 16)
        elif val_str.startswith("0b"):
            parsed_int = int(val_str, 2)
        elif mode in ("dec", "decimal") and re.fullmatch(r"[01]{4,}", val_str):
            parsed_int = int(val_str, 2)
        elif val_str.isdigit():
            parsed_int = int(val_str, 10)
        elif re.fullmatch(r"[0-9a-f]+", val_str):
            parsed_int = int(val_str, 16)
    elif convert_phrase:
        val_str, _target = convert_phrase.group(1), convert_phrase.group(2)
        if val_str.startswith("0x"):
            parsed_int = int(val_str, 16)
        elif val_str.startswith("0b"):
            parsed_int = int(val_str, 2)
        elif val_str.isdigit():
            parsed_int = int(val_str, 10)
        elif re.fullmatch(r"[0-9a-f]+", val_str):
            parsed_int = int(val_str, 16)

    if parsed_int is not None:
        answer = (
            f"**Number System Conversion**\n"
            f"• Decimal (Base 10): `{parsed_int}`\n"
            f"• Binary (Base 2): `{bin(parsed_int)}` (`{parsed_int:08b}` padded)\n"
            f"• Hexadecimal (Base 16): `{hex(parsed_int).upper().replace('0X', '0x')}`\n"
            f"• Octal (Base 8): `{oct(parsed_int)}`"
        )
        return _result(answer, category="Computer Science", steps="Exact base-2/8/10/16 conversion", tag="CS Number Base")

    # 3. Data Storage Unit Conversions (bits / bytes / KB / KiB / MB / MiB / GB / GiB / TB / TiB)
    storage_m = re.search(
        r"(\d+(?:\.\d+)?)\s*(bits?|bytes?|kib|mib|gib|tib|kb|mb|gb|tb)\s+(?:to|in|->)\s+(bits?|bytes?|kib|mib|gib|tib|kb|mb|gb|tb)\b",
        ql,
    )
    if storage_m:
        val = float(storage_m.group(1))
        src_u = storage_m.group(2).lower()
        dst_u = storage_m.group(3).lower()
        if src_u in _DATA_TO_BITS and dst_u in _DATA_TO_BITS:
            bits = val * _DATA_TO_BITS[src_u]
            res_val = bits / _DATA_TO_BITS[dst_u]
            answer = (
                f"**Data Storage Conversion**\n"
                f"• `{_fmt_num(val)} {storage_m.group(2)}` = **`{_fmt_num(res_val)} {storage_m.group(3)}`**\n"
                f"• Total Bits: `{_fmt_num(bits)} bits` | Bytes: `{_fmt_num(bits / 8.0)} B`"
            )
            steps = "SI units use powers of 1,000 (KB/MB/GB); IEC units use powers of 1,024 (KiB/MiB/GiB)."
            return _result(answer, category="Computer Science", steps=steps, tag="Storage Calc")

    # 4. Big-O Complexity Lookup
    if "big o" in ql or "big-o" in ql or "complexity" in ql:
        for key, info in _BIG_O_DB.items():
            if key in ql or (key == "quicksort" and "quick sort" in ql) or (key == "hash table" and "hashmap" in ql):
                answer = (
                    f"**Big-O Complexity: {info['name']}**\n"
                    f"• Best Time: `{info['best']}`\n"
                    f"• Average Time: `{info['average']}`\n"
                    f"• Worst Time: `{info['worst']}`\n"
                    f"• Space Complexity: `{info['space']}`\n"
                    f"• Note: {info['note']}"
                )
                return _result(answer, category="Computer Science", steps="Algorithmic complexity lookup", tag="Big-O Lookup")

    return None


def _try_general_math_and_units(q: str) -> Optional[Dict[str, Any]]:
    ql = q.lower().strip()

    # 0. Matrix Determinant & Inverse via NumPy (e.g., "matrix [[2,1],[5,3]]")
    mat_m = re.search(r"matrix\s*(\[\s*\[.+\]\s*\])", ql)
    if mat_m:
        try:
            raw_mat = ast.literal_eval(mat_m.group(1))
            arr = np.array(raw_mat, dtype=np.float64)
            if arr.ndim == 2 and arr.shape[0] == arr.shape[1] and arr.shape[0] <= 5:
                det = float(np.linalg.det(arr))
                lines = [
                    f"**Matrix Analysis ({arr.shape[0]}×{arr.shape[1]})**",
                    f"• Determinant: `{_fmt_num(det)}`",
                    f"• Trace: `{_fmt_num(float(np.trace(arr)))}`",
                ]
                if abs(det) > 1e-9:
                    inv = np.linalg.inv(arr)
                    inv_str = np.array2string(np.round(inv, 4), separator=", ")
                    lines.append(f"• Inverse (`A⁻¹`):\n`{inv_str}`")
                else:
                    lines.append("• Inverse: Singular matrix (det = 0, not invertible)")
                return _result("\n".join(lines), category="Math", steps="Computed via NumPy linalg", tag="Matrix Engine")
        except Exception:
            pass

    # 0b. Prime Check & Factorization (e.g., "isprime 97", "factors 360")
    prime_m = re.match(r"^(?:isprime|prime|factors?|factorize)\s+(\d+)$", ql)
    if prime_m:
        n = int(prime_m.group(1))
        if 2 <= n <= 10_000_000:
            factors: List[int] = []
            temp = n
            d = 2
            while d * d <= temp:
                while temp % d == 0:
                    factors.append(d)
                    temp //= d
                d += 1 if d == 2 else 2
            if temp > 1:
                factors.append(temp)
            is_p = len(factors) == 1
            f_str = " × ".join(str(x) for x in factors)
            answer = (
                f"**Number Theory: `{n}`**\n"
                f"• Is Prime? **`{'Yes' if is_p else 'No'}`**\n"
                f"• Prime Factorization: `{f_str}`"
            )
            return _result(answer, category="Math", steps="Trial division factorization", tag="Number Theory")

    # 1. Statistics (mean, median, stdev, variance, stats)
    stat_m = re.match(r"^(?:stats|statistics|mean|average|avg|median|stdev|std|variance|var)\b[:\s]*(.+)$", ql)
    if stat_m:
        nums = [float(x) for x in re.findall(r"[-+]?\d+(?:\.\d+)?", stat_m.group(1))]
        if len(nums) >= 2:
            n = len(nums)
            mean_v = statistics.mean(nums)
            median_v = statistics.median(nums)
            stdev_s = statistics.stdev(nums)
            var_s = statistics.variance(nums)
            cv_pct = (stdev_s / mean_v * 100.0) if mean_v != 0 else 0.0
            answer = (
                f"**Descriptive Statistics (n = {n})**\n"
                f"• Mean (x̄): `{_fmt_num(mean_v)}`\n"
                f"• Median: `{_fmt_num(median_v)}`\n"
                f"• Sample Std Dev (s): `{_fmt_num(stdev_s)}`\n"
                f"• Sample Variance (s²): `{_fmt_num(var_s)}`\n"
                f"• Coeff. of Variation (CV%): `{_fmt_num(cv_pct)}%`\n"
                f"• Min: `{_fmt_num(min(nums))}` | Max: `{_fmt_num(max(nums))}` | Sum: `{_fmt_num(sum(nums))}`"
            )
            steps = f"s = sqrt(Σ(x - {_fmt_num(mean_v)})² / ({n} - 1)) = {_fmt_num(stdev_s)}"
            return _result(answer, category="Math", steps=steps, tag="Statistics Engine")

    # 2. Quadratic & Linear Equation Solver
    # e.g. "solve 2x^2 - 5x + 2 = 0" or "x^2 - 5x + 6 = 0" or "3x + 9 = 0"
    eq_candidate = re.sub(r"^(?:solve|roots?\s+of)\s+", "", ql).strip()
    if "=" in eq_candidate and "x" in eq_candidate:
        parts = eq_candidate.split("=")
        if len(parts) == 2:
            lhs_s, rhs_s = parts[0].strip(), parts[1].strip()
            if re.fullmatch(r"[0-9xX\.\+\-\*\^\s\(\)]+", lhs_s) and re.fullmatch(r"[0-9xX\.\+\-\*\^\s\(\)]+", rhs_s):
                # Evaluate polynomial f(x) = LHS - RHS at x=0, 1, -1 to extract quadratic coefficients cleanly
                try:
                    def eval_poly(expr_s: str, x_val: float) -> float:
                        s = re.sub(r"(\d)\s*x", rf"\1*({x_val})", expr_s, flags=re.IGNORECASE)
                        s = re.sub(r"\bx\b", f"({x_val})", s, flags=re.IGNORECASE)
                        return safe_eval_math(s)

                    f0 = eval_poly(lhs_s, 0.0) - eval_poly(rhs_s, 0.0)
                    f1 = eval_poly(lhs_s, 1.0) - eval_poly(rhs_s, 1.0)
                    fm1 = eval_poly(lhs_s, -1.0) - eval_poly(rhs_s, -1.0)
                    c = f0
                    a = (f1 + fm1 - 2.0 * c) / 2.0
                    b = (f1 - fm1) / 2.0

                    if abs(a) > 1e-10:
                        disc = b * b - 4.0 * a * c
                        if disc > 1e-10:
                            r1 = (-b + math.sqrt(disc)) / (2.0 * a)
                            r2 = (-b - math.sqrt(disc)) / (2.0 * a)
                            roots_str = f"`x₁ = {_fmt_num(r1)}`, `x₂ = {_fmt_num(r2)}`"
                        elif abs(disc) <= 1e-10:
                            r1 = -b / (2.0 * a)
                            roots_str = f"`x = {_fmt_num(r1)}` (double real root)"
                        else:
                            real_p = -b / (2.0 * a)
                            imag_p = math.sqrt(-disc) / (2.0 * a)
                            roots_str = f"`x₁ = {_fmt_num(real_p)} + {_fmt_num(imag_p)}i`, `x₂ = {_fmt_num(real_p)} - {_fmt_num(imag_p)}i`"
                        answer = (
                            f"**Quadratic Equation Solution**\n"
                            f"• Standard Form: `{_fmt_num(a)}x² + ({_fmt_num(b)})x + ({_fmt_num(c)}) = 0`\n"
                            f"• Discriminant (Δ = b² - 4ac): `{_fmt_num(disc)}`\n"
                            f"• **Roots: {roots_str}**"
                        )
                        steps = "Solved using x = (-b ± √(b² - 4ac)) / (2a)"
                        return _result(answer, category="Math", steps=steps, tag="Algebra Solver")
                    elif abs(b) > 1e-10:
                        root = -c / b
                        answer = (
                            f"**Linear Equation Solution**\n"
                            f"• Standard Form: `{_fmt_num(b)}x + ({_fmt_num(c)}) = 0`\n"
                            f"• **Solution: `x = {_fmt_num(root)}`**"
                        )
                        steps = f"x = -({_fmt_num(c)}) / {_fmt_num(b)} = {_fmt_num(root)}"
                        return _result(answer, category="Math", steps=steps, tag="Algebra Solver")
                except Exception:
                    pass

    # 3. Temperature Conversions
    temp_m = re.search(
        r"([-+]?\d+(?:\.\d+)?)\s*°?\s*(c|celsius|f|fahrenheit|k|kelvin)\s+(?:to|in|->)\s+°?\s*(c|celsius|f|fahrenheit|k|kelvin)\b",
        ql,
    )
    if temp_m:
        val = float(temp_m.group(1))
        src = temp_m.group(2)[0].lower()
        dst = temp_m.group(3)[0].lower()
        c_val = val if src == "c" else ((val - 32.0) * 5.0 / 9.0 if src == "f" else val - 273.15)
        out_val = c_val if dst == "c" else (c_val * 9.0 / 5.0 + 32.0 if dst == "f" else c_val + 273.15)
        answer = f"**Temperature Conversion**\n• `{_fmt_num(val)} °{src.upper()}` = **`{_fmt_num(out_val)} °{dst.upper()}`**"
        return _result(answer, category="Math", steps="Exact thermodynamic scale conversion", tag="Unit Converter")

    # 4. Length, Area (incl. Ethiopian timad), Mass (incl. quintal) Conversions
    unit_m = re.search(
        r"(?:convert\s+)?(\d+(?:\.\d+)?)\s*([a-zA-Z0-9\^]+)\s+(?:to|in|->)\s+([a-zA-Z0-9\^]+)\b",
        ql,
    )
    if unit_m:
        val = float(unit_m.group(1))
        u1 = unit_m.group(2).lower()
        u2 = unit_m.group(3).lower()
        for table, label in ((_LENGTH_TO_M, "Length"), (_AREA_TO_M2, "Area"), (_MASS_TO_KG, "Mass")):
            if u1 in table and u2 in table:
                converted = val * table[u1] / table[u2]
                extra = ""
                if table is _AREA_TO_M2 and ("timad" in (u1, u2) or "ha" in (u1, u2)):
                    extra = "\n• *Reference: 1 hectare = 4 Ethiopian timad = 10,000 m²*"
                answer = (
                    f"**{label} Unit Conversion**\n"
                    f"• `{_fmt_num(val)} {unit_m.group(2)}` = **`{_fmt_num(converted)} {unit_m.group(3)}`**"
                    f"{extra}"
                )
                return _result(answer, category="Math", steps=f"Factor ratio: {table[u1]} / {table[u2]}", tag="Unit Converter")

    # 5. Natural-language Percentage ("15% of 240", "200 + 15%")
    pct_of = re.fullmatch(r"(\d+(?:\.\d+)?)\s*%\s*(?:of)\s*(\d+(?:\.\d+)?)", ql)
    if pct_of:
        p, base = float(pct_of.group(1)), float(pct_of.group(2))
        res = (p / 100.0) * base
        return _result(
            f"**Percentage Result**\n• `{_fmt_num(p)}% of {_fmt_num(base)}` = **`{_fmt_num(res)}`**",
            category="Math",
            steps=f"({p} / 100) × {base} = {_fmt_num(res)}",
            tag="Math AST",
        )

    # 6. Pure Scientific Math Expression via AST
    math_candidate = re.sub(r"^(?:calculate|compute|eval|what\s+is)\s+", "", q.strip(), flags=re.IGNORECASE).rstrip("?").strip()
    # Replace "200 + 15%" -> "200 + (200 * 0.15)" or standalone "15%" -> "(15/100)"
    math_candidate = re.sub(r"(\d+(?:\.\d+)?)\s*%", r"(\1/100.0)", math_candidate)

    has_math_signal = (
        any(op in math_candidate for op in ("+", "-", "*", "/", "^", "√", "!"))
        or any(fn in math_candidate.lower() for fn in tuple(_SAFE_FUNCS.keys()))
    )
    if has_math_signal and not re.search(r"\b(what|why|how|explain|define|describe|tell)\b", ql):
        try:
            val = safe_eval_math(math_candidate)
            formatted = _fmt_num(val)
            return _result(
                f"**Result:** `{formatted}`",
                category="Math",
                steps=f"AST Evaluated: `{math_candidate}` = `{formatted}`",
                tag="Safe AST Math",
            )
        except Exception:
            pass

    return None


def evaluate_query(query: str) -> Optional[Dict[str, Any]]:
    """
    Attempt to solve the user query deterministically using the AST math engine,
    unit conversions, statistics, Horticulture calculators, or CS calculators.
    Returns None if the query is not a mathematical/calculator request.
    """
    if not query or not query.strip():
        return None

    for handler in (
        _try_horticulture_calculators,
        _try_cs_calculators,
        _try_general_math_and_units,
    ):
        res = handler(query)
        if res is not None:
            return res
    return None

from flask import Flask, render_template, request

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    if request.method == "POST":
        try:
            # Dane wejściowe!
            points = float(request.form["points"])
            publication_type = request.form["publication_type"]
            wiz_count = int(request.form["wiz_count"])
            total_count = int(request.form["total_count"])

            # Obliczenia
            slot_value, points_value = calculate_slots_and_points(points, publication_type, wiz_count, total_count)

            # Zaokrąglanie wyników
            slot_value = round(slot_value, 4)
            points_value = round(points_value, 4)

            # Wynik
            result = {
                "points": points,
                "publication_type": publication_type,
                "wiz_count": wiz_count,
                "total_count": total_count,
                "slots": slot_value,
                "calculated_points": points_value,
            }
        except Exception as e:
            result = {"error": str(e)}

    return render_template("index.html", result=result)


def calculate_slots_and_points(points, publication_type, wiz_count, total_count):
    slot_value, points_value = 0, 0

    if publication_type.lower() in ["artykuł", "artykul"]:
        if points in [200, 140, 100] and wiz_count > 0:
            slot_value = 1 / wiz_count
            points_value = slot_value * points
        elif points in [70, 40]:
            if wiz_count == total_count and wiz_count > 0:
                slot_value = 1 / wiz_count
            else:
                slot_value = ((wiz_count / total_count) ** 0.5) / wiz_count if wiz_count > 0 else 0
            points_value = slot_value * points
        elif points in [20, 5] and total_count > 0:
            slot_value = 1 / total_count
            points_value = slot_value * points
    elif publication_type.lower() in ["rozdział", "ksiazka", "książka"]:
        if points in [300, 150, 75] and wiz_count > 0:
            slot_value = 1 / wiz_count
            points_value = slot_value * points
        elif points in [120, 40, 20]:
            if wiz_count == total_count and wiz_count > 0:
                slot_value = 1 / wiz_count
            else:
                slot_value = ((wiz_count / total_count) ** 0.5) / wiz_count if wiz_count > 0 else 0
            points_value = slot_value * points
        elif points in [20, 5] and total_count > 0:
            slot_value = 1 / total_count
            points_value = slot_value * points

    return slot_value, points_value


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

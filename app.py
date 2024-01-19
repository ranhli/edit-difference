from flask import Flask, render_template, request, jsonify

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/check_difference", methods=["POST"])
def check_difference():
    data = request.get_json()
    sentence1 = data["sentence1"]
    sentence2 = data["sentence2"]

    difference = edit_distance(sentence1, sentence2)

    return jsonify({"difference": difference})


def edit_distance(str1, str2):
    m, n = len(str1), len(str2)

    dp = [[0] * (n + 1) for _ in range(m + 1)]

    for i in range(m + 1):
        for j in range(n + 1):
            if i == 0:
                dp[i][j] = j
            elif j == 0:
                dp[i][j] = i
            elif str1[i - 1] == str2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]
            else:
                dp[i][j] = 1 + min(
                    dp[i - 1][j],
                    dp[i][j - 1],
                    dp[i - 1][j - 1],
                )

    return dp[m][n]


if __name__ == "__main__":
    app.run(debug=False)

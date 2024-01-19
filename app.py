from flask import Flask, render_template, request, jsonify
import difflib

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/check_difference", methods=["POST"])
def check_difference():
    data = request.get_json()
    sentence1 = data["sentence1"]
    sentence2 = data["sentence2"]

    res1, res2 = edit_distance(sentence1, sentence2)

    return jsonify({"sentence1": res1, "sentence2": res2})


def edit_distance(sentence1, sentence2):
    matcher = difflib.SequenceMatcher(None, sentence1.split(), sentence2.split())

    marked_sentence1 = []
    marked_sentence2 = []
    print(matcher.get_opcodes())
    for opcode, start1, end1, start2, end2 in matcher.get_opcodes():
        if opcode == "equal":
            marked_sentence1.extend(sentence1.split()[start1:end1])
            marked_sentence2.extend(sentence2.split()[start2:end2])
        elif opcode == "replace":
            sub1 = sentence1.split()[start1:end1]
            sub2 = sentence2.split()[start2:end2]
            list1_indxes, list2_indxes, prefixes = find_shared_prefix_pairs(sub1, sub2)
            for i in range(len(sub1)):
                if i in list1_indxes:
                    print(sub1[i])
                    length = prefixes[list1_indxes.index(i)]
                    sub1[i] = (
                        sub1[i][0:length]
                        + f"<mark id='remove'>{sub1[i][length:]}</mark>"
                    )
                else:
                    sub1[i] = f"<mark id='remove'>{sub1[i]}</mark>"
            for j in range(len(sub2)):
                if j in list2_indxes:
                    length = prefixes[list2_indxes.index(j)]
                    sub2[j] = (
                        sub2[j][0:length] + f"<mark id='add'>{sub2[j][length:]}</mark>"
                    )
                else:
                    sub2[j] = f"<mark id='add'>{sub2[j]}</mark>"
            marked_sentence1.append(" ".join(sub1))
            marked_sentence2.append(" ".join(sub2))
        elif opcode == "delete":
            marked_sentence1.extend(
                [
                    f"<mark id='remove'>{word}</mark>"
                    for word in sentence1.split()[start1:end1]
                ]
            )
        elif opcode == "insert":
            marked_sentence2.extend(
                [
                    f"<mark id='add'>{word}</mark>"
                    for word in sentence2.split()[start2:end2]
                ]
            )

    return " ".join(marked_sentence1), " ".join(marked_sentence2)


def find_shared_prefix_pairs(list1, list2):
    list1_indexes = []
    list2_indexes = []
    prefix_lengths = []
    max_j = 0

    for i, str1 in enumerate(list1):
        for j, str2 in enumerate(list2):
            prefix_length = 0
            min_length = min(len(str1), len(str2))

            while (
                prefix_length < min_length
                and str1[prefix_length].lower() == str2[prefix_length].lower()
            ):
                prefix_length += 1

            if prefix_length > 1 and j >= max_j:
                list1_indexes.append(i)
                list2_indexes.append(j)
                max_j = j
                prefix_lengths.append(prefix_length)

    return list1_indexes, list2_indexes, prefix_lengths


if __name__ == "__main__":
    app.run(debug=True)

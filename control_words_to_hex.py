#!./venv/bin/python
from sys import argv

CONTROL_WORDS = {"IO","MI","RW","RO","CO","CE","J","CODEI","RANDI","RANDO","BI","BO","AI","AO"}

CONTROL_WORDS_DICT = {
    "IO":    0b1000000000000000,
    "MI":    0b0100000000000000,
    "RW":    0b0010000000000000,
    "RO":    0b0001000000000000,
    "CO":    0b0000100000000000,
    "CE":    0b0000010000000000,
    "J":     0b0000001000000000,
    "CODEI": 0b0000000100000000,
    "RANDI": 0b0000000010000000,
    "RANDO": 0b0000000001000000,
    # Reserved
    # Reserved
    "BI":    0b0000000000001000,
    "BO":    0b0000000000000100,
    "AI":    0b0000000000000010,
    "AO":    0b0000000000000001
}


def control_word_to_int(control_word: str):
    return CONTROL_WORDS_DICT[control_word]


def control_words_to_hex(control_words: set[str]) -> str:
    result: str = ""

    for control_word in control_words:
        if control_word not in CONTROL_WORDS:
            raise ValueError("Control Word does not exist")
        pass
    
    word_values: set[int] = set()
    for control_word in control_words:
        word_values.add(control_word_to_int(control_word))

    words_value: int = 0
    for word_value in word_values:
        words_value += word_value

    result: str = hex(words_value).lstrip("0x")
    return result


def main():
    def dump_to_file(filename, results):
        with open(filename, "w+") as f:
            if len(argv) >= 2 and argv[1] == "--digital":
                f.write("v2.0 raw\n")
            for result in results:
                f.write(result)
                f.write("\n")
            pass
        pass
    
    end: bool = False
    results: list[str] = []
    while not end:
        result: str = ""
        comma_seperated_input: str = input("Enter Control Words(comma seperated)(Enter \"end\" (unqouted) to end)(Enter \"dump\" (unqouted) to dump values to a file):")
        if comma_seperated_input == "end":
            print("bye")
            end = True
            break
        elif comma_seperated_input == "dump":
            filename = input("Enter file name to save:")
            try:
                dump_to_file(filename, results)
                print(f"Successfully dumped results to file: {filename}")
                end = True
                break
            except IsADirectoryError:
                raise ValueError("File is a directory")
            except:
                raise ValueError("File I/O error")

        control_words: list[str] = comma_seperated_input.split(",")
        result = control_words_to_hex(set(control_words))
        results.append(result)
        print(result)
        


if(__name__ == '__main__'):
    main()

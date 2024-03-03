class Options:
    def choose(opt_names:list[str], input_ask_value="Choose option") -> int:
        comment = ""
        while True:
            for i, n in enumerate(opt_names):
                print(f"[{i+1}] {n}")
            print("\n" + comment)
            o = input(input_ask_value.strip() + " ")
            try:
                o = int(o)
            except TypeError:
                comment = "Please type an intieger number"
                continue
            except Exception as e:
                print(e)

            return o
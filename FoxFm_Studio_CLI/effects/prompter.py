class Prompter:
    def ask_user(questions:list[str], param_names:list[str], values_types:list) -> dict:
        if len(questions) != len(values_types):
            print("**WARINING: NOT THE SAME NUMBER OF QUESTIONS AND VALUES**")
        
        values = []
        for i, q in enumerate(questions):
            while True:
                v = input(q + " ")
                try:
                    v = values_types[i](v)
                    values.append(v)
                except TypeError:
                    print(f"Please insert value of type {values_types[i].__name__}")
                    continue
                except Exception as e:
                    print(e)
                
                break
        
        res = dict(zip(param_names, values))
        return res

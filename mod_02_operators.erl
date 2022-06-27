-module(mod_02_operators).

-export([main/0]).

main() -> main(-2, 5).

main(A, B) ->
    if A < B ->
        io:fwrite("~w is ~s\n", [ A, number_name(A) ]),
        main(A+1, B)
    ;  true -> ok % ok is used as empty statement
    end.

number_name(X) ->
    if X =< -1 -> "less then zero"
    ;  X == 0  -> "zero"
    ;  X == 1  -> "one"
    ;  X == 2  -> "two"
    ;  X == 3  -> "three"
    ;  X >= 4  -> "at least 4"
    end.

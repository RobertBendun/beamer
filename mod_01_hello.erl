-module(mod_01_hello).

-export([main/0]).

main() ->
    io:fwrite("hello, world\n"),
    io:fwrite("goodbye, world!\n").
$fibonacci
.fun_start
    $n
    .fvar

    @n
    !1
    .gt
    .not
    .if_start
        .cb
        @n
        .fun_stop
    .if_end
    .cb

    @n
    !-1
    .sum
    .fibonacci
    $ret1
    .fvar

    @n
    !-2
    .sum
    .fibonacci
    @ret1
    .sum
.fun_end


$main
.fun_start
    !0
    $i
    .var

    .rep_start
        @i
        .print
        .cb
        $\t\t
        .compile_str
        .print
        .cb

        @i
        .fibonacci
        .print
        .cb
        .print

        @i
        !1
        .sum
        $i
        .var
    .rep_end
.fun_end


.main


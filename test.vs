$err_fun
.fun_start
    $n
    .fvar

    @n
    !2
    .sum
    $b
    .fvar

    @b
    .print
    .cb
    .print

    @n
    !0
    .eq
    .if_start
        .cb
        .not
    .if_end

    .cb
    @n
    !-1
    .sum
    .err_fun
.fun_end


!10
$number
.var

@number
.err_fun
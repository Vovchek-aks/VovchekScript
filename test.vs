$\n
.compile_str
$n
.var

!0
$i
.var

.rep_start
    @i
    .print
    .cb
    @n
    .print
    .cb

    !1
    $i
    .sum_to
    .cb

    @i
    !10
    .eq
    .if_start
        .cb
        $stop
        .print
        .rep_stop
    .if_end
    .cb
.rep_end
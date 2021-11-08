.input
.int
$max
.var

!0
$i
.var

.rep_start
    @i
    .print
    .cb
    .print

    !1
    @i
    .sum
    $i
    .var

    !0
    $n
    .var

    .rep_start
        @n
        .print
        .cb
        .space
        .print
        .cb

        !1
        @n
        .sum
        $n
        .var

        @n
        @i
        .eq
        .if_start
            .cb
            .print
            .rep_stop
        .if_end
        .cb
    .rep_end
    .cb

    @i
    @max
    .eq
    .if_start
        .rep_stop
    .if_end
    .cb
.rep_end
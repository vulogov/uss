;
; Here is our shared memory segments configuration
;

(deftemplate shared_memory_segment
    ; Segment name
    (slot key
        (type STRING)
        (default ?DERIVE)
    )
    ; Segment ID
    (slot id
        (type NUMBER)
        (default 1)
    )
    ; Maximum number of Elements
    (slot max_elements
        (type NUMBER)
        (default 1)
    )
    ; Maximum number of Elements
    (slot max_element_size
        (type NUMBER)
        (default 1024)
    )
    ; Maximum of the element key
    (slot max_key_length
        (type NUMBER)
        (default 128)
    )
)


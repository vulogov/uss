;;
;; Application setup
;;
(application
    (name "test application")
    (desc "test application description")
    (poc "Vladimir Ulogov")
    (email "vladimir.ulogov@zabbix.com")
    (phone "+1-973-555-1122")
)
;;
;; Modules setup
;;
(pcbind
    (name "Main PYCLP bindings")
    (path "/root/SHARED/Src/uss/etc/bind")
)
(py_module
    (name "Main PY modules")
    (path "/root/SRC/uss/etc/ini/py/")
)

;;
;; Startup
;;
(start
    (name "dummy.main")
    (desc "Dummy startup code")
)

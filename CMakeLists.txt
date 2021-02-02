cmake_minimum_required(VERSION 2.6)
project(uspd)

find_package(PkgConfig REQUIRED)
find_package(CURL REQUIRED)
find_package(ZLIB REQUIRED)
pkg_check_modules(OpenSSL openssl REQUIRED)
pkg_check_modules(ARES libcares REQUIRED)
pkg_check_modules(SQL REQUIRED sqlite3)
#pkg_check_modules(MOSQUITTOPP REQUIRED libmosquittopp)
#pkg_check_modules(MOSQUITTO REQUIRED libmosquitto)

include_directories(${CURL_INCLUDE_DIR})
include_directories(${ZLIB_INCLUDE_DIR})
include_directories(${CMAKE_CURRENT_SOURCE_DIR}/src/protobuf-c/)
include_directories(${CMAKE_CURRENT_SOURCE_DIR}/src/vendor/)
include_directories(${CMAKE_CURRENT_SOURCE_DIR}/src/include/)
include_directories(${CMAKE_CURRENT_SOURCE_DIR}/src/libjson/ccan/json/)

set(OBUSPA_LOCAL_STATE_DIR /tmp)

SET(TARGET_SRC
    src/core/main.c
    src/core/mtp_exec.c
    src/core/dm_exec.c
    src/core/bdc_exec.c
    src/core/stomp.c
    src/core/socket_set.c
    src/core/msg_handler.c
    src/core/handle_get.c
    src/core/handle_set.c
    src/core/handle_add.c
    src/core/handle_delete.c
    src/core/handle_notify.c
    src/core/handle_operate.c
    src/core/handle_get_supported_protocol.c
    src/core/handle_get_instances.c
    src/core/handle_get_supported_dm.c
    src/core/group_get_vector.c
    src/core/group_set_vector.c
    src/core/proto_trace.c
    src/core/data_model.c
    src/core/error_resp.c
    src/core/usp_register.c
    src/core/usp_api.c
    src/core/dm_access.c
    src/core/device_local_agent.c
    src/core/device_controller.c
    src/core/device_mtp.c
    src/core/device_stomp.c
    src/core/device_subscription.c
    src/core/device_security.c
    src/core/device_ctrust.c
    src/core/device_bulkdata.c
    src/core/device_selftest_example.c
    src/core/device_time.c
    src/core/uptime.c
    src/core/rfc1123.c
    src/core/database.c
    src/core/usp_err.c
    src/core/usp_log.c
    src/core/usp_mem.c
    src/core/nu_ipaddr.c
    src/core/nu_macaddr.c
    src/core/retry_wait.c
    src/core/path_resolver.c
    src/core/str_vector.c
    src/core/int_vector.c
    src/core/kv_vector.c
    src/core/dm_inst_vector.c
    src/core/expr_vector.c
    src/core/dm_trans.c
    src/core/subs_vector.c
    src/core/subs_retry.c
    src/core/sync_timer.c
    src/core/cli_server.c
    src/core/cli_client.c
    src/core/iso8601.c
    src/core/text_utils.c
    src/core/os_utils.c
    src/core/device_request.c
    src/core/dllist.c
    src/core/coap_common.c
    src/core/coap_client.c
    src/core/coap_server.c
    src/core/uri.c
    src/core/mqtt.c
    src/core/device_mqtt.c
    src/vendor/vendor.c
    src/vendor/vendor_factory_reset_example.c
    src/libjson/ccan/json/json.c
    src/protobuf-c/protobuf-c.c
    src/protobuf-c/usp-msg.pb-c.c
    src/protobuf-c/usp-record.pb-c.c
    )

set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} -DENABLE_COAP")
#set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} -DENABLE_MQTT")
set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} -DOBUSPA_LOCAL_STATE_DIR=\"tmp\"")
set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} -Werror -Werror=unused-value -Werror=format -Winit-self -Wparentheses -Werror=parentheses -Wuninitialized -Werror=uninitialized -Wpointer-arith")

add_executable(uspd ${TARGET_SRC})
target_link_libraries(uspd ${SQL_LIBRARIES} ${MOSQUITTO_LIBRARIES} ${MOSQUITTOPP_LIBRARIES} ${ZLIB_LIBRARIES} ${CURL_LIBRARIES} ${SQLITE3_LIBRARIES} ${ARES_LIBRARIES} ${OpenSSL_LIBRARIES} -lm -ldl -lpthread -lrt  )

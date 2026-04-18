from typing import Final

ENCODINGS: Final =          ("utf-8-sig","utf-8","utf-16","utf-16-le","utf-16-be","cp1250","cp1251","cp1252","cp1254","latin-1","iso-8859-2","iso-8859-1","iso-8859-15","cp850","cp852","cp437","mac_roman","koi8-r","shift_jis","gbk","utf-32",) # most common encodings

HOST_MAPPING: Final =       {
                            "host name": "host_name",
                            "primary dns suffix": "primary_dns_suffix",
                            "node type": "node_type",
                            "ip routing enabled": "ip_routing_enabled",
                            "wins proxy enabled": "wins_proxy_enabled",
                            "dns suffix search list": "dns_search_list",
                            }

ADAPTER_MAPPING: Final =    {
                            # IPV4
                            "ipv4 address": "ipv4_address",
                            "autoconfiguration ipv4 address": "ipv4_address",

                            # IPV6
                            "ipv6 address": "ipv6_address",
                            "temporary ipv6 address": "ipv6_temporary",
                            "link-local ipv6 address": "ipv6_link_local",

                            # NETWORK
                            "subnet mask": "subnet_mask",
                            "default gateway": "default_gateway",

                            # DHCP
                            "dhcp enabled": "dhcp_enabled",
                            "dhcp server": "dhcp_server",

                            # LEASE
                            "lease obtained": "lease_obtained",
                            "lease expires": "lease_expires",

                            # DNS
                            "dns servers": "dns_servers",
                            "connection-specific dns suffix": "dns_suffix",

                            # DEVICE INFO
                            "description": "description",
                            "physical address": "physical_address",

                            # DHCPv6
                            "dhcpv6 iaid": "dhcpv6_iaid",
                            "dhcpv6 client duid": "dhcpv6_duid",

                            # STATE
                            "media state": "media_state",
                            "netbios over tcpip": "netbios_over_tcpip",
                            "autoconfiguration enabled": "autoconfiguration_enabled",
                        }

IMPORTANT_FIELDS: Final =["adapter_name","description","physical_address","dhcp_enabled","ipv4_address","subnet_mask","default_gateway","dns_servers",]

LIST_FIELDS: Final =    {"default_gateway","dns_servers",}
BAD_GATEWAYS: Final =   {"127.0.0.1","192.168.0.1","::1",}
# This file is part of the sos project: https://github.com/sosreport/sos
#
# This copyrighted material is made available to anyone wishing to use,
# modify, copy, or redistribute it subject to the terms and conditions of
# version 2 of the GNU General Public License.
#
# See the LICENSE file in the source distribution for further information.

from sos.report.plugins import Plugin, IndependentPlugin


class Scst(Plugin, IndependentPlugin):
    """SCST (SCSI Target Subsystem) is a set of Linux kernel drivers that
    implement SCSI target functionality for exporting storage over protocols
    such as iSCSI, Fibre Channel, and SRP.

    This plugin collects SCST configuration files, running configuration
    via scstadmin, sysfs state from /sys/kernel/scst_tgt/, and service
    status for both scst and iscsi-scst services.
    """

    short_desc = 'SCST SCSI target subsystem'

    plugin_name = 'scst'
    profiles = ('storage',)
    kernel_mods = ('scst',)
    commands = ('scstadmin',)

    def setup(self):
        self.add_copy_spec([
            "/etc/scst.conf",
            "/etc/default/scst",
            "/etc/sysconfig/scst",
            "/sys/kernel/scst_tgt/version",
            "/sys/kernel/scst_tgt/threads",
            "/sys/kernel/scst_tgt/trace_level",
            "/sys/kernel/scst_tgt/trace_cmds",
            "/sys/kernel/scst_tgt/trace_mcmds",
            "/sys/kernel/scst_tgt/last_sysfs_mgmt_res",
            "/sys/kernel/scst_tgt/sgv/",
            "/sys/kernel/scst_tgt/handlers/",
            "/sys/kernel/scst_tgt/devices/",
            "/sys/kernel/scst_tgt/targets/",
            "/sys/kernel/scst_tgt/device_groups/",
        ])

        self.add_cmd_output([
            "scstadmin -list_handler",
            "scstadmin -list_device",
            "scstadmin -list_driver",
            "scstadmin -list_target",
            "scstadmin -list_dgrp",
            "scstadmin -list_sessions",
            "scstadmin -list_scst_attr",
            "scstadmin -write_config /dev/stdout",
        ])

        self.add_cmd_output("ls -laR /var/lib/scst/pr/",
                            suggest_filename="scst_pr_listing")

        self.add_service_status("scst")
        self.add_service_status("iscsi-scst")

    def postproc(self):
        # Scrub CHAP passwords from IncomingUser/OutgoingUser lines
        # Format: IncomingUser "user password" or OutgoingUser "user password"
        self.do_path_regex_sub(
            "/etc/scst.conf",
            r"((?:IncomingUser|OutgoingUser)\s+\S+)\s+\S+(.*)",
            r"\1 ********\2"
        )

# vim: set et ts=4 sw=4 :

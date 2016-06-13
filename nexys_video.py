#!/usr/bin/env python3

from nexys_base import *

from litex.soc.interconnect import stream

from litevideo.output import VideoOut
from litedram.common import LiteDRAMPort
from litedram.frontend.adaptation import LiteDRAMPortCDC, LiteDRAMPortUpConverter

from litescope import LiteScopeAnalyzer

base_cls = MiniSoC


class VideoOutSoC(base_cls):
    csr_map = {
        "hdmi_out0": 21,
        "analyzer":  22
    }
    csr_map.update(base_cls.csr_map)

    def __init__(self, platform, *args, **kwargs):
        base_cls.__init__(self, platform, *args, **kwargs)

        # # #


        mode = "ycbcr422"

        if mode == "ycbcr422":
            hdmi_out0_dram_port = self.sdram.crossbar.get_port(16, "pix")
            self.submodules.hdmi_out0 = VideoOut(platform.device,
                                                 platform.request("hdmi_out"),
                                                 hdmi_out0_dram_port,
                                                 "ycbcr422")
        elif mode == "rgb":
            hdmi_out0_dram_port = self.sdram.crossbar.get_port(32, "pix")
            self.submodules.hdmi_out0 = VideoOut(platform.device,
                                                 platform.request("hdmi_out"),
                                                 hdmi_out0_dram_port,
                                                 "rgb")

        self.platform.add_false_path_constraints(
            self.crg.cd_sys.clk,
            self.hdmi_out0.driver.clocking.cd_pix.clk)

        analyzer_signals = [
            hdmi_out0_dram_port.cmd.valid,
            hdmi_out0_dram_port.cmd.ready,
            hdmi_out0_dram_port.cmd.we,
            hdmi_out0_dram_port.cmd.adr,
            hdmi_out0_dram_port.wdata.valid,
            hdmi_out0_dram_port.wdata.ready,
            #hdmi_out0_dram_port.wdata.data,
            hdmi_out0_dram_port.wdata.we,
            hdmi_out0_dram_port.rdata.valid,
            hdmi_out0_dram_port.rdata.ready,
            #hdmi_out0_dram_port.rdata.data,
            self.hdmi_out0.driver.sink.valid,
            self.hdmi_out0.driver.sink.de,
            self.hdmi_out0.driver.sink.hsync,
            self.hdmi_out0.driver.sink.vsync,
            self.hdmi_out0.driver.sink.r,
            self.hdmi_out0.driver.sink.g,
            self.hdmi_out0.driver.sink.b
        ]
        self.submodules.analyzer = LiteScopeAnalyzer(analyzer_signals, 2048, cd="pix", cd_ratio=2)


def main():
    parser = argparse.ArgumentParser(description="Nexys LiteX SoC")
    builder_args(parser)
    soc_sdram_args(parser)
    parser.add_argument("--nocompile-gateware", action="store_true")
    args = parser.parse_args()

    platform = nexys.Platform()
    soc = VideoOutSoC(platform, **soc_sdram_argdict(args))
    builder = Builder(soc, output_dir="build",
                      compile_gateware=not args.nocompile_gateware,
                      csr_csv="test/csr.csv")
    vns = builder.build()
    soc.analyzer.export_csv(vns, "test/analyzer.csv")

if __name__ == "__main__":
    main()


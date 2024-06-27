from opentrons import protocol_api
from typing import Literal

metadata = {
    "protocolName": "Template Protocol",
    "author": "ikeda042",
    "description": "A template protocol for OpenTrons.",
    "apiLevel": "2.18",
}


class LabwareLoader:
    def __init__(self, protocol: protocol_api.ProtocolContext) -> None:
        self.protocol = protocol

    def get_tiprack(
        self,
        tiprack_type: Literal[
            "opentrons_96_tiprack_300ul", "opentrons_96_tiprack_20ul"
        ],
        slot: Literal["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12"],
    ) -> protocol_api.labware.Labware:
        return self.protocol.load_labware(tiprack_type, slot)

    def load_plate(
        self,
        plate_type: Literal["corning_96_wellplate_360ul_flat"],
        slot: Literal["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12"],
    ) -> protocol_api.labware.Labware:
        return self.protocol.load_labware(plate_type, slot)

    def load_pipette(
        self,
        pipette_type: Literal["p300_multi_gen2", "p20_multi_gen2"],
        tiprack: protocol_api.labware.Labware,
        mount: Literal["left", "right"],
    ) -> protocol_api.InstrumentContext:
        return self.protocol.load_instrument(pipette_type, mount, tip_racks=[tiprack])


class OpenTronsProtocol:
    def __init__(self, protocol: protocol_api.ProtocolContext) -> None:
        self.protocol = protocol
        self.labware_loader = LabwareLoader(protocol)
        self.wells: list[str] = [
            "A1",
            "B1",
            "C1",
            "D1",
            "E1",
            "F1",
            "G1",
            "H1",
            "A2",
            "B2",
            "C2",
            "D2",
            "E2",
            "F2",
            "G2",
            "H2",
            "A3",
            "B3",
            "C3",
            "D3",
            "E3",
            "F3",
            "G3",
            "H3",
            "A4",
            "B4",
            "C4",
            "D4",
            "E4",
            "F4",
            "G4",
            "H4",
            "A5",
            "B5",
            "C5",
            "D5",
            "E5",
            "F5",
            "G5",
            "H5",
            "A6",
            "B6",
            "C6",
            "D6",
            "E6",
            "F6",
            "G6",
            "H6",
            "A7",
            "B7",
            "C7",
            "D7",
            "E7",
            "F7",
            "G7",
            "H7",
            "A8",
            "B8",
            "C8",
            "D8",
            "E8",
            "F8",
            "G8",
            "H8",
            "A9",
            "B9",
            "C9",
            "D9",
            "E9",
            "F9",
            "G9",
            "H9",
            "A10",
            "B10",
            "C10",
            "D10",
            "E10",
            "F10",
            "G10",
            "H10",
            "A11",
            "B11",
            "C11",
            "D11",
            "E11",
            "F11",
            "G11",
            "H11",
            "A12",
            "B12",
            "C12",
            "D12",
            "E12",
            "F12",
            "G12",
            "H12",
        ]
        self.pick_up_from: list[str] = ['A1', 'B1', 'C1']

    def exec(self) -> None:
        tiprack = self.labware_loader.get_tiprack("opentrons_96_tiprack_300ul", "7")
        right_pipette = self.labware_loader.load_pipette(
            "p300_multi_gen2", tiprack, "right"
        )
        microplate = self.labware_loader.load_plate(
            "corning_96_wellplate_360ul_flat", "2"
        )
        self.perform_pipetting_cycle(
            right_pipette,
            tiprack,
            microplate,
        )

    def perform_pipetting_cycle(
        self,
        pipette: protocol_api.InstrumentContext,
        tiprack: protocol_api.labware.Labware,
        plate: protocol_api.labware.Labware,
    ) -> None:

        for fr, to in zip(self.wells, self.wells):
            pipette.pick_up_tip(tiprack.wells_by_name()[to])
            pipette.aspirate(150, plate.wells_by_name()[fr])
            pipette.dispense(150, plate.wells_by_name()[to])
            pipette.blow_out()
            pipette.drop_tip()


def run(protocol: protocol_api.ProtocolContext) -> None:
    ot_protocol = OpenTronsProtocol(protocol)
    ot_protocol.exec()

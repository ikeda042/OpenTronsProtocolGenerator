from opentrons import protocol_api
from typing import Literal
import requests
from datetime import datetime, timedelta, timezone

JST: timezone = timezone(timedelta(hours=+9))

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


class Messenger:
    def __init__(self, protocol: protocol_api.ProtocolContext) -> None:
        self.protocol = protocol

    def send_message(self, message: str) -> None:
        url = (
            "http://localhost:8000/send_message"
            if self.protocol.is_simulating()
            else "http://10.32.17.122:8000/send_message"
        )
        try:
            response = requests.post(url, json={"message": message})
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")

    @staticmethod
    def get_current_time() -> str:
        return datetime.now(JST).strftime("%Y-%m-%d %H:%M:%S")


class OpenTronsProtocol:
    def __init__(self, protocol: protocol_api.ProtocolContext) -> None:
        self.protocol = protocol
        self.labware_loader = LabwareLoader(protocol)
        self.messenger = Messenger(protocol)

    def exec(self) -> None:
        tiprack = self.labware_loader.get_tiprack("opentrons_96_tiprack_300ul", "7")
        right_pipette = self.labware_loader.load_pipette(
            "p300_multi_gen2", tiprack, "right"
        )
        pool = self.labware_loader.load_plate("corning_96_wellplate_360ul_flat", "6")
        microplate = self.labware_loader.load_plate(
            "corning_96_wellplate_360ul_flat", "2"
        )

        self.messenger.send_message(
            f"*{self.messenger.get_current_time()}* 分注操作を開始します。"
        )
        self.perform_pipetting_cycle(
            right_pipette,
            tiprack,
            pool,
            microplate,
        )

        self.messenger.send_message(
            f"*{self.messenger.get_current_time()}* 全ての処理が完了しました。"
        )

    def perform_pipetting_cycle(
        self,
        pipette: protocol_api.InstrumentContext,
        tiprack: protocol_api.labware.Labware,
        pool: protocol_api.labware.Labware,
        plate: protocol_api.labware.Labware,
    ) -> None:
        pipette.pick_up_tip(tiprack.wells_by_name()["A1"])
        # self.messenger.send_message(
        #     f"*{self.messenger.get_current_time()}* 区画7のラックの1列目からチップを取りました。"
        # )
        for n in range(1, 13):
            pipette.aspirate(150, pool.wells_by_name()["A1"])
            # self.messenger.send_message(
            #     f"*{self.messenger.get_current_time()}* 区画6の培地プールから8つのピペット全てに150uLの培地を吸引しました。"
            # )

            pipette.dispense(150, plate.wells_by_name()[f"A{n}"])
            # self.messenger.send_message(
            #     f"*{self.messenger.get_current_time()}* 区画2のマイクロプレートリーダーの{n}列目の全ウェルに150uLの溶液を移動しました。"
            # )

        pipette.drop_tip(tiprack.wells_by_name()["A1"])
        # self.messenger.send_message(
        #     f"*{self.messenger.get_current_time()}* チップを区画7のラックの1列目に戻しました。"
        # )


def run(protocol: protocol_api.ProtocolContext) -> None:
    ot_protocol = OpenTronsProtocol(protocol)
    ot_protocol.exec()

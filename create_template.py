"""
This script generates ISA-PHM (Investigation/Study/Assay for Prognostics and
Health Management) templates from a provided JSON file containing the
necessary metadata. It leverages the isatools library to construct ISA-Tab or
ISA-JSON representations of experimental investigations, studies, assays
and associated metadata such as sensors, test setups, file details
and fault/degradation protocols.

Classes:
    FileParameter: Represents a protocol parameter and its value for a file.
    FileDetails: Holds information about a data file, including names,
                 locations, parameters, and labels.
    Sensor: Describes a sensor used in the experiment, including its type,
            unit, and technical details.
    TestSetUp: Contains details about the experimental setup, including
               sensors and their characteristics.
    AssayInfo: Holds information about an assay, including the sensor used and
               file details.
    StudyInfo: Aggregates all metadata for a study, including title, contacts,
               setup, faults, and assays.
    IsaPhmInfo: Top-level container for investigation metadata, including
                studies, contacts, and publications.

Functions:
    create_info(filename) -> IsaPhmInfo:
        Parses the input JSON file and returns an IsaPhmInfo object with all
        relevant metadata.

    create_study_descriptor(experiment_type):
        Creates an ontology annotation for the study's experiment type.

    add_test_setup(study: Study, study_info: StudyInfo):
        Adds test setup sources and samples to the study based on provided
        setup information.

    create_assay_data(assay_info: AssayInfo, sample: Sample, study: Study,
                      s_index: int, test_setup: TestSetUp):
        Constructs assay data, including protocols, processes, and data files,
        and links them to the sample.

    create_fault_preparation_protocol(study: Study, study_info: StudyInfo):
        Adds a fault/degradation preparation protocol and process to the study.

    create_study_data(study_info: StudyInfo, index: int):
        Assembles all study-level metadata, including samples, factors,
        protocols, and assays.

    create_isa_data(IsaPhmInfo: IsaPhmInfo):
        Builds the full ISA investigation object from the IsaPhmInfo metadata.

    main(args):
        Entry point for the script. Parses arguments, loads metadata,
        generates ISA structures, and writes output files.

Usage:
    Run the script with a JSON file containing investigation metadata:
        python create_template.py [options] <input_file.json>

    Options:
        -t, --tab    Output ISA-Tab format (default: True)
        -j, --json   Output ISA-JSON format (default: False)

Dependencies:
    - isatools
    - argparse
    - dataclasses
    - typing

Note:
    The script expects the input JSON file to conform to the structure
    required by the IsaPhmInfo class and its nested components.
    If imported to another python file and an IsaPhmInfo object is made you can
    use the function create_isa_data to create the investigation object.
"""
from dataclasses import dataclass, field
from typing import List
from isatools.model import *
from isatools import isatab
from isatools.isatab.dump.write import *
import argparse


@dataclass
class FileParameter:
    parameter: ProtocolParameter
    value: ParameterValue


@dataclass
class FileDetails:
    """
    This class will hold the information of a file.
    """
    raw_file_name: str = ""
    raw_file_location: str = ""
    proccesed_file_name: str = ""
    proccesed_file_location: str = ""
    file_parameters: List[FileParameter] = field(default_factory=list)  # filter information
    number_of_columns: str = 0
    labels: List[str] = field(default_factory=list)  # Column labels
    # Column 1 label [incl. unit] = "Sample nr. [-]""
    # Column 2 label [incl. unit] = "Filtered Vibration level [g]"


@dataclass
class Sensor:
    """
    This class will hold the information of a sensor.
    """
    identifier: str = "s0"
    measurement_type: str = ""
    measurement_unit: str = ""
    description: str = ""
    # Sensor details
    technology_type: str = ""
    technology_platform: str = ""
    data_acquisition_unit: str = ""
    sampling_rate: str = ""
    sampeling_unit: str = ""
    sensor_location: str = ""
    location_unit: str = ""
    sensor_orientation: str = ""
    orientation_unit: str = ""


@dataclass
class TestSetUp:
    name: str = ""
    location: str = ""
    characteristics: List[Characteristic] = field(default_factory=list)
    # Sensors and Measurements
    number_of_sensors: int = 0
    sensors: List[Sensor] = field(default_factory=list)


@dataclass
class AssayInfo:
    """
    This class will hold the information of an assay.
    """
    used_sensor: Sensor
    file_details: FileDetails


@dataclass
class StudyInfo:
    title: str = ""
    description: str = ""
    submission_date: str = ""
    public_release_date: str = ""
    detail_preparation: str = ""
    publication: Publication = None
    # STUDY CONTACTS
    contacts: List[Person] = field(default_factory=list)
    experiment_type: str = ""  # Diagnostic, Degradation-constant, Degradation-time-varyingstant
    # Setup
    used_setup: TestSetUp = None
    # Fault / Degradation
    fault_type: str = ""  # Fault, Degradation
    fault_position: str = ""  # Position of the fault
    fault_severity: str = ""  # Severity of the fault, can be an integer or a string
    operating_conditions: List[FactorValue] = field(default_factory=list)
    assay_details: List[AssayInfo] = field(default_factory=list)


@dataclass
class IsaPhmInfo:
    """
    This class will hold the information generated by a frontend.
    Any dates should be in ISO 8601 format.

    Attributes:
        identifier: The identifier of the investigation.
        title: The title of the investigation.
        description: The description of the investigation.
        submission_date: The submission date of the investigation.
        public_release_date: The public release date of the investigation.
        publication: The publication of the investigation.
        contacts: The contacts of the investigation.
        study_details: The details of the studies in the investigation.
    """
    identifier: str = "i0"
    title: str = ""
    description: str = ""
    submission_date: str = ""
    public_release_date: str = ""
    # INVESTIGATION PUBLICATIONS
    publication: Publication = None
    # INVESTIGATION CONTACTS
    contacts: List[Person] = field(default_factory=list)
    # INVESTIGATION STUDIES
    study_details: List[StudyInfo] = field(default_factory=list)


def create_info(filename) -> IsaPhmInfo:
    """
    Parses the input JSON file and returns an IsaPhmInfo object with all
    relevant metadata.
    """
    # TODO: Implement JSON parsing logic
    pass


def create_study_descriptor(experiment_type):
    """
    Creates an ontology annotation for the study's experiment type.
    """
    annotation = OntologyAnnotation(term=experiment_type)
    return annotation


def add_test_setup(study: Study, study_info: StudyInfo):
    """
    Adds test setup sources and samples to the study based on provided
    setup information.
    """
    source = Source(name=study_info.used_setup.name)
    study.sources.append(source)
    sample = Sample(
        name=f"{study_info.fault_type}_{study_info.fault_position}_{study_info.fault_severity}",
        derives_from=[source])
    sample.characteristics = study_info.used_setup.characteristics
    sample.factor_values.extend(study_info.operating_conditions)
    study.samples = [sample]
    return sample


def create_assay_data(assay_info: AssayInfo, sample: Sample, study: Study,
                      s_index:int, test_setup: TestSetUp):
    """
    Constructs assay data, including protocols, processes, and data files,
    and links them to the sample.
    """
    assay = Assay()
    # Sensor Details
    sensor = assay_info.used_sensor
    assay.filename = f"a_assay_st{s_index}_se{test_setup.sensors.index(sensor)}.txt"
    assay.measurement_type = OntologyAnnotation(sensor.measurement_type)
    assay.technology_type = OntologyAnnotation(sensor.technology_type)
    assay.technology_platform = sensor.technology_platform
    SR = ProtocolParameter(parameter_name=OntologyAnnotation("sampling rate"))
    SL = ProtocolParameter(parameter_name=OntologyAnnotation("Sensor location"))
    SO = ProtocolParameter(parameter_name=OntologyAnnotation("Sensor orientation"))
    MU = ProtocolParameter(parameter_name=OntologyAnnotation("Measured unit"))
    DataAcquisition = ProtocolParameter(parameter_name=OntologyAnnotation("Data Acquisition Unit"))
    SR_value = ParameterValue(category=SR, value=sensor.sampling_rate,
                              unit=OntologyAnnotation(sensor.sampeling_unit))
    SL_value = ParameterValue(
        category=SL, value=sensor.sensor_location)
    SO_value = ParameterValue(category=SO, value=sensor.sensor_orientation)
    MU_value = ParameterValue(category=MU, value=sensor.measurement_unit)
    DataAcquisition_value = ParameterValue(
        category=DataAcquisition, value=sensor.data_acquisition_unit)

    file_details = assay_info.file_details
    data_collection_protocol = Protocol(
        name="data collection",
        protocol_type="data collection",
        parameters=[SR, SL, SO, MU, DataAcquisition])

    study.protocols.append(data_collection_protocol)

    data_collection_process = Process(
        executes_protocol=data_collection_protocol,
        parameter_values=[SR_value, SL_value, SO_value, MU_value,
                          DataAcquisition_value]
    )

    datafile_raw = DataFile(
        filename=file_details.raw_file_name,
        label="Raw Data File",
        generated_from=[sample],
    )

    data_collection_process.inputs.append(sample)
    data_collection_process.outputs.append(datafile_raw)
    assay.process_sequence.append(data_collection_process)

    if file_details.file_parameters:
        data_transformation_protocol = Protocol(
            name="data transformation",
            protocol_type="data transformation",
            parameters=[file_parameter.parameter for
                        file_parameter in file_details.file_parameters])
        study.protocols.append(data_transformation_protocol)

        data_transformation_process = Process(
            executes_protocol=data_transformation_protocol,
            parameter_values=[file_parameter.value for
                              file_parameter in file_details.file_parameters])
        data_transformation_process.inputs.append(
            data_collection_process.outputs[0])
        datafile = DataFile(
            filename=file_details.proccesed_file_name,
            label="Derived Array Data File",
            generated_from=[sample])
        data_transformation_process.outputs.append(datafile)
        plink(data_collection_process, data_transformation_process)
        assay.process_sequence.append(data_transformation_process)

    assay.samples.append(sample)

    return assay


def create_fault_preparation_protocol(study: Study, study_info: StudyInfo):
    """
    Adds a fault/degradation preparation protocol and process to the study.
    """

    # Define ProtocolParameters for factors
    f_params = []
    f_params_val = []
    if study_info.experiment_type == "Diagnostic":
        FT_param = ProtocolParameter(parameter_name=OntologyAnnotation(term="Fault Type"))
        FP_param = ProtocolParameter(parameter_name=OntologyAnnotation(term="Fault Position"))
        FS_param = ProtocolParameter(parameter_name=OntologyAnnotation(term="Fault Severity"))
        FT_value = ParameterValue(category=FT_param, value=study_info.fault_type)
        FP_value = ParameterValue(category=FP_param, value=study_info.fault_position)
        FS_value = ParameterValue(category=FS_param, value=study_info.fault_severity)
        f_params = [FT_param, FP_param, FS_param]
        f_params_val = [FT_value, FP_value, FS_value]

    experiment_preparation_protocol = Protocol(
        name=study_info.detail_preparation,
        protocol_type=OntologyAnnotation(term="Fault/degradation protocol"),
        parameters=f_params
    )

    study.protocols.append(experiment_preparation_protocol)

    # Define ParameterValues for the process

    experiment_preparation_process = Process(
        executes_protocol=experiment_preparation_protocol,
        parameter_values=f_params_val
    )

    for src in study.sources:
        experiment_preparation_process.inputs.append(src)
    for sam in study.samples:
        experiment_preparation_process.outputs.append(sam)

    study.process_sequence.append(experiment_preparation_process)


def create_study_data(study_info: StudyInfo, index: int):
    """
    Assembles all study-level metadata, including samples, factors,
    protocols, and assays.
    """
    study = Study(filename=f"s_study_s{index}.txt")
    study.title = study_info.title
    study.identifier = f"s{index}"
    study.description = study_info.description
    study.submission_date = study_info.submission_date
    study.public_release_date = study_info.public_release_date
    # STUDY PUBLICATIONS
    if study_info.publication:
        study.publications.append(study_info.publication)
    # STUDY CONTACTS
    study.contacts = study_info.contacts
    # Experiment type
    study.design_descriptors.append(create_study_descriptor(study_info.experiment_type))
    # Study design
    sample = add_test_setup(study, study_info)

    # # Fault / Degradation
    if study_info.experiment_type != "Diagnostic":
        FT = StudyFactor(name="Fault Type", factor_type=study_info.experiment_type)
        FP = StudyFactor(name="Fault Position", factor_type=study_info.experiment_type)
        FS = StudyFactor(name="Fault Severity", factor_type=study_info.experiment_type)
        FT1 = FactorValue(factor_name=FT, value=study_info.fault_type)
        FP1 = FactorValue(factor_name=FP, value=study_info.fault_position)
        FS1 = FactorValue(factor_name=FS, value=study_info.fault_severity)
        sample.factor_values.append(FT1)
        sample.factor_values.append(FP1)
        sample.factor_values.append(FS1)
    
    f_type = "Fault" if study_info.experiment_type == "Diagnostic" else "Load"
    study.add_factor(name="Fault Type", factor_type=f_type)
    study.add_factor(name="Fault Position", factor_type=f_type)
    study.add_factor(name="Fault Severity", factor_type=f_type)

    # Protocol refrerence
    create_fault_preparation_protocol(study, study_info)

    for assay in study_info.assay_details:
        assay_data = create_assay_data(assay, sample, study, index, study_info.used_setup)
        study.assays.append(assay_data)

    return study


def create_isa_data(IsaPhmInfo: IsaPhmInfo):
    """
    Builds the full ISA investigation object from the IsaPhmInfo metadata.
    """
    investigation = Investigation()
    investigation.filename = "i_investigation.txt"
    investigation.identifier = IsaPhmInfo.identifier
    investigation.title = IsaPhmInfo.title
    investigation.description = IsaPhmInfo.description
    investigation.submission_date = IsaPhmInfo.submission_date
    investigation.public_release_date = IsaPhmInfo.public_release_date
    # INVESTIGATION PUBLICATIONS
    if IsaPhmInfo.publication:
        investigation.publications.append(IsaPhmInfo.publication)
    # INVESTIGATION CONTACTS
    investigation.contacts = IsaPhmInfo.contacts
    for i, study in enumerate(IsaPhmInfo.study_details):
        s = create_study_data(study, i)
        investigation.studies.append(s)
    return investigation


def main(args):
    """
    Entry point for the script. Parses arguments, loads metadata,
    generates ISA structures, and writes output files.
    """
    info = create_info(args.file)
    inv_obj = create_isa_data(info)
    write_study_table_files(inv_obj, "")  # ,write_factor_values=False)
    write_assay_table_files(
        inv_obj, "", write_factor_values=False
    )  # ,write_factor_values=False)
    isatab.dump(inv_obj)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--tab", action="store_true", default=True,
                        help="when this is flag is enabled outputs isa-tab format, default is True")
    parser.add_argument("-j", "--json", action="store_true", default=False,
                        help="when this is flag is enabled outputs isa-json format, default is False")
    parser.add_argument("file",
                        help="input a json file that contains the necessary information to create the isa-phm")
    args = parser.parse_args()
    main(args)

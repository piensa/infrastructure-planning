from argparse import ArgumentParser
from crosscompute_table import TableType
from invisibleroads_macros.disk import make_enumerated_folder_for, make_folder
from os.path import join


def run(target_folder, *args):
    electricity_consumption_by_year_table = \
        estimate_consumption_from_curve(*args)
    electricity_consumption_by_year_table_path = join(
        target_folder, 'electricity-consumption-by-year.csv')
    electricity_consumption_by_year_table.to_csv(
        electricity_consumption_by_year_table_path, index=False)
    return [(
        'electricity_consumption_by_year_table_path',
        electricity_consumption_by_year_table_path,
    )]


def estimate_consumption_from_curve(
        demographic_by_year_table,
        demographic_by_year_table_name_column,
        demographic_by_year_table_year_column,
        demographic_by_year_table_population_column,
        consumption_by_population_table,
        consumption_by_population_table_population_column,
        consumption_by_population_table_consumption_column):
    # return consumption_by_year_table
    pass


if __name__ == '__main__':
    argument_parser = ArgumentParser()
    argument_parser.add_argument(
        '--target_folder',
        metavar='FOLDER', type=make_folder)

    argument_parser.add_argument(
        '--demographic_by_year_table_path',
        metavar='PATH', required=True)
    argument_parser.add_argument(
        '--demographic_by_year_table_name_column',
        metavar='COLUMN', required=True)
    argument_parser.add_argument(
        '--demographic_by_year_table_year_column',
        metavar='COLUMN', required=True)
    argument_parser.add_argument(
        '--demographic_by_year_table_population_column',
        metavar='COLUMN', required=True)

    argument_parser.add_argument(
        '--electricity_consumption_by_population_table_path',
        metavar='PATH', required=True)
    argument_parser.add_argument(
        '--electricity_consumption_by_population_table_population_column',
        metavar='COLUMN', required=True)
    argument_parser.add_argument(
        '--electricity_consumption_by_population_table_consumption_column',
        metavar='COLUMN', required=True)

    args = argument_parser.parse_args()
    d = run(
        args.target_folder or make_enumerated_folder_for(__file__),

        TableType.load(
            args.demographic_by_year_table_path),
        args.demographic_by_year_table_name_column,
        args.demographic_by_year_table_year_column,
        args.demographic_by_year_table_population_column,

        TableType.load(
            args.electricity_consumption_by_population_table_path),
        args.electricity_consumption_by_population_table_population_column,
        args.electricity_consumption_by_population_table_consumption_column)
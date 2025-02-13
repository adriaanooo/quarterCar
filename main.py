from quarter_car import QuarterCar
from data_handling import params_from_excel, write_to_excel
from plotting import plot_data, animate_data
from input_profile import sweep_60s_40Hz, road_bump


def main():

    # Grab data from excel sheet.
    m1, m2, k1, c1, k2 = params_from_excel('excel_files/inputs.xlsx')

    # Set run time and resolution
    time = int(input("\nRun time (s): "))
    n_samples = int(input("Samples: "))

    # Create quarter-car instance
    my_car = QuarterCar(m1, m2, k1, c1, k2, input_profile=sweep_60s_40Hz, time=time, n_samples=n_samples)
    my_car.print_vehicle_params()

    # Write displacements to excel sheet
    write_to_excel('excel_files/outputs.xlsx', my_car.t, my_car.sprung_disp, my_car.unsprung_disp)

    # Show results.
    plot_data(my_car.t, my_car.sprung_disp, my_car.unsprung_disp, my_car.input_profile)
    #animate_data(time, n_samples, my_car.t, my_car.sprung_disp, my_car.unsprung_disp, my_car.input_profile)


if __name__ == '__main__':
    main()

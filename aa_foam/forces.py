# coding: utf-8

r"""OpenFOAM computed forces handling"""

from typing import Tuple, List, Dict


def force_line2values(line: str) -> Tuple[float, ...]:
    r"""Convert a line of a postProcessing/forces.dat file to numeric values

    Parameters
    ----------
    line : line from postProcessing/forces/<timestep>/force.dat

    """
    tokens_unprocessed = line.split()
    tokens = [x.replace(")", "").replace("(", "") for x in tokens_unprocessed]
    floats = [float(x) for x in tokens]
    time, ftx, fty, ftz, fpx, fpy, fpz, fvx, fvy, fvz = \
        floats[0], floats[1], floats[2], floats[3], floats[4], floats[5], \
        floats[6], floats[7], floats[8], floats[9]

    return (time,
            ftx, fty, ftz,
            fpx, fpy, fpz,
            fvx, fvy, fvz)


def force_line2values_old_format(line: str) -> Tuple[float, ...]:
    r"""Convert a line of a postProcessing/forces/<timestep>/forces.dat file to numeric values
    for an older format where forces and moments are in the same file

    Parameters
    ----------
    line : line from postProcessing/forces/<timestep>/forces.dat

    """
    tokens_unprocessed = line.split()
    tokens = [x.replace(")", "").replace("(", "") for x in tokens_unprocessed]
    floats = [float(x) for x in tokens]
    time, fpx, fpy, fpz, fvx, fvy, fvz, fpox, fpoy, fpoz, \
        mpx, mpy, mpz, mvx, mvy, mvz, mpox, mpoy, mpoz = \
        floats[0], floats[1], floats[2], floats[3], floats[4], floats[5], \
        floats[6], floats[7], floats[8], floats[9], \
        floats[10], floats[11], floats[12], floats[13], floats[14], \
        floats[15], floats[16], floats[17], floats[18]

    return (time,
            fpx, fpy, fpz,
            fvx, fvy, fvz,
            fpox, fpoy, fpoz,
            mpx, mpy, mpz,
            mvx, mvy, mvz,
            mpox, mpoy, mpoz)


def force_data(forcefile_name: str,
               old_format: bool,
               avg_last: int = 100) -> Tuple[List[float], List[List[float]], List[str], Dict[str, float]]:
    r"""Retrieve force data.

    Returns
    -------
    List of times
    List of list of values
    List of titles for the lists of values, in the same order as the list of list of values
    A dictionary where the key is a title and the value is the average
    over the last avg_last iterations.

    """
    times, ftxs, ftys, ftzs, fpxs, fpys, fpzs, fvxs, fvys, fvzs, fpoxs, fpoys, fpozs = \
        [], [], [], [], [], [], [], [], [], [], [], [], []

    with open(forcefile_name) as fd:
        for line in fd:
            if line[0] == "#":
                continue
            if old_format is False:
                time, ftx, fty, ftz, fpx, fpy, fpz, fvx, fvy, fvz = \
                    force_line2values(line)
                times.append(time)
                ftxs.append(ftx)
                ftys.append(fty)
                ftzs.append(ftz)
                fpxs.append(fpx)
                fpys.append(fpy)
                fpzs.append(fpz)
                fvxs.append(fvx)
                fvys.append(fvy)
                fvzs.append(fvz)
                ys = [ftxs, ftys, ftzs, fpxs, fpys, fpzs, fvxs, fvys, fvzs]
                titles = ['Ft x', 'Ft y', 'Ft z', 'Fp x', 'Fp y', 'Fp z', 'Fv x', 'Fv y', 'Fv z']
            else:
                time, fpx, fpy, fpz, fvx, fvy, fvz, fpox, fpoy, fpoz, \
                    _, _, _, _, _, _, _, _, _ = force_line2values_old_format(line)
                times.append(time)
                fpxs.append(fpx)
                fpys.append(fpy)
                fpzs.append(fpz)
                fvxs.append(fvx)
                fvys.append(fvy)
                fvzs.append(fvz)
                fpoxs.append(fpox)
                fpoys.append(fpoy)
                fpozs.append(fpoz)
                ys = [fpxs, fpys, fpzs, fvxs, fvys, fvzs, fpoxs, fpoys, fpozs]
                titles = ['Fp x', 'Fp y', 'Fp z', 'Fv x', 'Fv y', 'Fv z', 'Fpoxs', 'Fpoys', 'Fpozs']
    # Compute averages
    averages = {}
    for y, title in zip(ys, titles):
        averages[title] = float(sum(y[-avg_last:-1]) / len(y[-avg_last:-1]))

    return times, ys, titles, averages

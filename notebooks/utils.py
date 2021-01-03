import QuantLib as ql
import pandas as pd


def to_dates(dates):
    return [d.to_date() for d in dates]


def get_spot_rates(yield_curve, day_count, calendar=ql.UnitedStates(), months=121):
    spots = []
    tenors = []
    ref_date = yield_curve.referenceDate()
    calc_date = ref_date
    for month in range(0, months):
        yrs = month / 12.
        d = calendar.advance(ref_date, ql.Period(month, ql.Months))
        compounding = ql.Compounded
        freq = ql.Semiannual
        zero_rate = yield_curve.zeroRate(yrs, compounding, freq)
        tenors.append(yrs)
        eq_rate = zero_rate.equivalentRate(day_count, compounding, freq, calc_date, d).rate()
        spots.append(100 * eq_rate)
    return pd.DataFrame(list(zip(tenors, spots)), columns=["Maturity", "Curve"], index=[""]*len(tenors))

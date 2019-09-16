# (c) Kevin Dunn, 2019. MIT License.


# import statsmodels.api as sm
import warnings
import numpy as np
import pandas as pd
import statsmodels.formula.api as smf
from statsmodels.regression.linear_model import OLS
from statsmodels.iolib.summary import Summary

from plotting import paretoPlot
from datasets import data
from structures import c, expand, gather


class Model(OLS):
    """
    Just a thin wrapper around the OLS class from Statsmodels."""
    def __init__(self, OLS_instance):
        self._OLS = OLS_instance

    def summary(self, alpha=0.05, print_to_screen=True):
        """
        Side effect: prints to the screen.
        """
        # Taken from statsmodels.regression.linear_model.py
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            smry = self._OLS.summary()

        if np.isinf(self._OLS.scale):
            se = (f"Residual standard error: --- on {int(self._OLS.df_resid)} "
                  "degrees of freedom.")
        else:
            se = (f"Residual standard error: {np.sqrt(self._OLS.scale)} on "
                  f"{int(self._OLS.df_resid)} degrees of freedom.")

        smry.add_extra_txt([se])
        # if print_to_screen:
        #     print(smry)

        return smry


def lm(model_spec: str, data: pd.DataFrame) -> Model:
    """
    """
    model = smf.ols(model_spec, data=data).fit()
    out = Model(OLS_instance=model)
    return out


def summary(model: Model):
    """
    Prints a summary to the screen of the model.
    """
    return model.summary()


if __name__ == '__main__':

    # 3B
    A = c(-1, +1, -1, +1)
    B = c(-1, -1, +1, +1, name='B')
    y = c(52, 74, 62, 80)

    expt = gather(A=A, B=B, y=y)
    popped_corn = lm("y ~ A + B + A*B", expt)
    summary(popped_corn)

    # 3C
    C = T = S = c(-1, +1)
    C, T, S = expand.grid(C=C, T=T, S=S)
    y = c(5, 30, 6, 33, 4, 3, 5, 4)
    expt = gather(C=C, T=T, S=S, y=y)

    water = lm("y ~ C * T * S", expt)
    summary(water)

    paretoPlot(water)

    # 3D
    solar = data("solar")
    model_y1 = lm("y1 ~ A*B*C*D", data=solar)
    summary(model_y1)
    paretoPlot(model_y1)

    model_y2 = lm("y2 ~ A*B*C*D", data=solar)
    summary(model_y2)
    paretoPlot(model_y2)
    paretoPlot(model_y2, main="Pareto plot for Energy Delivery Efficiency")

    # 4H
    A = B = C = c(-1, +1)
    A, B, C = expand.grid(A=A, B=B, C=C)

    # These 4 factors are generated, using the trade-off table relationships
    D = A*B
    E = A*C
    F = B*C
    G = A*B*C

    # These are the 8 experimental outcomes, corresponding to the 8 entries
    # in each of the vectors above
    y = c(320, 276, 306, 290, 272, 274, 290, 255)

    expt = gather(A=A, B=B, C=C, D=D, E=E, F=F, G=G, y=y)

    # And finally, the linear model
    mod_ff = lm("y ~ A*B*C*D*E*F*G", expt)
    paretoPlot(mod_ff)

    # Now rebuild the linear model with only the 4 important terms
    mod_res4 = lm("y ~ A*C*E*G", expt)
    paretoPlot(mod_res4)

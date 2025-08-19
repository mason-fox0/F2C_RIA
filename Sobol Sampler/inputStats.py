import polars as pl

def main():
    schemaDef = {'fuel_cond_scale'  : pl.Float64,
                 'fuel_cp_scale'    : pl.Float64,
                 'clad_cond_scale'  : pl.Float64,
                 'clad_cp_scale'    : pl.Float64,
                 'pulse_width'      : pl.Float64,
                 'nb_multiplier'    : pl.Float64,
                 'chf_multiplier'   : pl.Float64,
                 'trans_multiplier' : pl.Float64,
                 'fb_multiplier'    : pl.Float64,
                 'gas_cond_scale'   : pl.Float64
            }

    lf = pl.scan_csv("inputParams.csv", schema=schemaDef)

    with pl.Config(tbl_cols=-1):
        print(lf.collect().describe())

if __name__ == "__main__":
    main()

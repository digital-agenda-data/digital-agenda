select
    d.code as dataset,
    case
        when dvi.code = 'E_IGOV2' then 'E_IGOV'
        when dvi.code = 'E_IGOV3' then 'E_IGOV'
        when dvi.code = 'E_IGOV2RT' then 'E_IGOVRT'
        when dvi.code = 'E_IGOV2PR' then 'E_IGOVPR'
        when dvi.code = 'E_INV2' then 'E_INV'
--         when dvi.code = 'E_IACC3G' then 'E_PMD'
--         when dvi.code = 'E_IACC3G_20' then 'E_EMPMD_GT20'
        when dvi.code = 'E_ERP' then 'E_ERP1'
        when dvi.code = 'P_IACC3G' then 'P_EMPMD'
        when dvi.code = 'P_EMPMD1' then 'P_EMPMD'
        when dvi.code = 'P_EMPMD2' then 'P_EMPMD'
        when dvi.code = 'E_EMPMD1_GT0' then 'E_PMD'
        when dvi.code = 'E_EMPMD2_GT0' then 'E_PMD'
        when dvi.code = 'E_EMPMD1_GT20' then 'E_EMPMD_GT20'
        when dvi.code = 'E_EMPMD2_GT20' then 'E_EMPMD_GT20'
        when dvi.code = 'E_ENVRA' then 'E_RA'
        when dvi.code = 'E_SM1_ANY' then 'E_SM_ANY'
        when dvi.code = 'E_RFID1' then 'E_RFID'
        when dvi.code = 'E_SM1_GE2' then 'E_SM_GE2'
        when dvi.code = 'E_RFAC1' then 'E_RFAC'
        when dvi.code = 'E_RFPSAS1' then 'E_RFPSAS'
        when dvi.code = 'E_EBUY2' then 'E_EBUY'
        when dvi.code = 'E_INVSNDAP' then 'E_INVSND'
        when dvi.code = 'E_INV3SBG_AP_GT0' then 'E_INVSND'
        when dvi.code = 'E_FIXBB' then 'E_BROAD'
        when dvi.code = 'E_SECPOL' then 'E_SECPOL1'
        else dvi.code
    end as indicator,
    case
        when dvb.code = '10_C10_S951_XK' then 'ENT_ALL_XFIN'
        when dvb.code = 'SM_C10_S951_XK' then 'ENT_SM_XFIN'
        when dvb.code = 'S_C10_S951_XK' then 'ENT_S_XFIN'
        when dvb.code = 'M_C10_S951_XK' then 'ENT_M_XFIN'
        when dvb.code = 'L_C10_S951_XK' then 'ENT_L_XFIN'
        else dvb.code
    end as breakdown,
    dvu.code as unit,
    case
        when dvc.code = 'EU27_2020' then 'EU'
        else dvc.code
    end as country,
    dvp.code as period,
    f.value as fact,
    f.flags as flags
from estat_facts f
    join estat_datasets d on d.id = f.dataset_id
    join estat_dim_values dvi on dvi.id = f.indicator_id
    join estat_dim_values dvb on dvb.id = f.breakdown_id
    join estat_dim_values dvu on dvu.id = f.unit_id
    join estat_dim_values dvc on dvc.id = f.country_id
    join estat_dim_values dvp on dvp.id = f.period_id
where
    dvc.code in ('AT', 'BE', 'BG', 'CY', 'CZ', 'DE', 'DK', 'EE', 'EL', 'ES', 'FI', 'FR', 'HR', 'HU', 'IE', 'IS', 'IT', 'LT', 'LU', 'LV', 'MT', 'NL', 'NO', 'PL', 'PT', 'RO', 'SE', 'SI', 'SK', 'UK', 'EU27_2020')
    and dvu.code in (
      'PC_ENT',
      'PC_TURN',
      'PC_ENT_ITSPRCR2',
      'PC_EMP',
      'PC_EMP_PMD',
      'PC_ENT_AESELL'
    )
    and dvp.code > '2000'
    and dvb.code in (
      '10_C10_18',
      '10_C10_S951_XK',
      '10_C19_23',
      '10_C24_25',
      '10_C26_33',
      '10_D35_E39',
      '10_F41_43',
      '10_G45',
      '10_G46',
      '10_G47',
      '10_H49_53',
      '10_I55_56',
      '10_J58_60',
      '10_J61',
      '10_J62_63',
      '10_L68',
      '10_M69_74',
      '10_N77_82',
      'L_C10_F43',
      'L_C10_S951_XK',
      'L_G45_S951_XK',
      'M_C10_F43',
      'M_C10_S951_XK',
      'M_G45_S951_XK',
      'S_C10_F43',
      'S_C10_S951_XK',
      'S_G45_S951_XK',
      'SM_C10_S951_XK'
    )
    and dvi.code in (
      'E_ADE',
      'E_ADS',
      'E_ADS_LOC',
      'E_ADS_TRK',
      'E_AESEU',
      'E_AWS_CMP',
      'E_AWS_COWN',
      'E_AWS_GT1_B2C_GT10WS',
      'E_AWSVAL_CMP',
      'E_AWSVAL_COWN',
      'E_BD',
      'E_BDA',
      'E_BROAD',
      'E_CC',
      'E_CC_GE_ME',
      'E_CRMAN',
      'E_EBUY2',
      'E_EMPMD1_GT0',
      'E_EMPMD1_GT20',
      'E_EMPMD_GT20',
      'E_ENVRA',
      'E_ERP',
      'E_ERP1',
      'E_ESELL',
      'E_ETURN',
      'E_FIXBB',
      'E_IACC3G',
      'E_IACC3G_20',
      'E_IGOV',
      'E_IGOV2',
      'E_IGOV3',
      'E_IGOVPR',
      'E_IGOV2PR',
      'E_IGOVRT',
      'E_IGOV2RT',
      'E_INV',
      'E_INV2',
      'E_INV4S_AP',
      'E_INV3SBG_AP_GT0',
      'E_INVSNDAP',
      'E_ISPDF_GE30',
      'E_ISPDFOKX',
      'E_ISPDFOKX_GE100',
      'E_IT_MEXT',
      'E_ITSP2',
      'E_ITSPVAC2',
      'E_ITT2',
      'E_PMD',
      'E_PMD_APP',
      'E_RA',
      'E_RFAC',
      'E_RFAC1',
      'E_RFID',
      'E_RFID1',
      'E_RFPSAS',
      'E_RFPSAS1',
      'E_SECPOL',
      'E_SECPOL1',
      'E_SISC',
      'E_SISORP',
      'E_SM1_ANY',
      'E_SM1_GE2',
      'E_SM_ANY',
      'E_SM_GE2',
      'E_WEB',
      'E_WEBF2',
      'E_WSEL25',
      'E_WSEL50' ,
      'P_EMPMD',
      'P_EMPMD1',
      'P_EMPMD2',
      'P_IACC3G',
      'P_IUSE',
      'E_EBUY',
      'E_CC1_SI',
      'E_AI_TANY',
      'E_DI3_HI',
      'E_DI3_LO',
      'E_DI3_VHI',
      'E_DI3_VLO'
    )
order by dataset, indicator, breakdown, unit, country, period;

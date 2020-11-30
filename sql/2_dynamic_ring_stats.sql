create table dynamic_ring_stats
(
    id             bigint primary key,
    file           bigint           not null references files,
    clfs           smallint         not null,
    metric         smallint         not null references metrics,
    mapping        smallint         not null references mappings,
    mv_acc         double precision not null,
    mv_precisionMi double precision not null,
    mv_recallMi    double precision not null,
    mv_fScoreMi    double precision not null,
    mv_precisionM  double precision not null,
    mv_recallM     double precision not null,
    mv_fScoreM     double precision not null,
    rf_acc         double precision not null,
    rf_precisionMi double precision not null,
    rf_recallMi    double precision not null,
    rf_fScoreMi    double precision not null,
    rf_precisionM  double precision not null,
    rf_recallM     double precision not null,
    rf_fScoreM     double precision not null,
    i_acc          double precision not null,
    i_precisionMi  double precision not null,
    i_recallMi     double precision not null,
    i_fScoreMi     double precision not null,
    i_precisionM   double precision not null,
    i_recallM      double precision not null,
    i_fScoreM      double precision not null,
    ir_acc         double precision not null,
    ir_precisionMi double precision not null,
    ir_recallMi    double precision not null,
    ir_fScoreMi    double precision not null,
    ir_precisionM  double precision not null,
    ir_recallM     double precision not null,
    ir_fScoreM     double precision not null
);
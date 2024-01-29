from uuid import UUID

from celery import chain, chord

import src.db.crud as crud
from src.analyzer import ECGAnalyzer, BackendChallengeECGAnalyzer
from src.celery.main import celery_app
from src.schemas import ECGSubmission


@celery_app.task
def async_analyze_ecg_leads(ecg: ECGSubmission,
                            user_id: UUID,
                            analyzer: ECGAnalyzer = BackendChallengeECGAnalyzer()):
    async_ecg_create(ecg, user_id=user_id)
    main_workflow = [async_analyze.s(lead.signal, analyzer=analyzer) for lead in ecg.leads]
    callback_workflow = chain(
        async_count_zero_crosses.s() |
        async_ecg_create_analysis.s(ecg_id=ecg.id) |
        async_ecg_update_analysis_by_id.si(ecg_id=ecg.id)
    )
    return chord(header=main_workflow, body=callback_workflow).delay()


@celery_app.task
def async_analyze(signal: list[int], analyzer: ECGAnalyzer):
    return analyzer.analyze(signal)


@celery_app.task
def async_count_zero_crosses(lead_analyzer_results: list[int]):
    return sum(lead_analyzer_results)


@celery_app.task
def async_ecg_create(ecg: ECGSubmission, user_id: UUID):
    crud.ecg_create(ecg=ecg,
                    user_id=user_id)


@celery_app.task
def async_ecg_create_analysis(zero_crosses_count: int, ecg_id: UUID):
    crud.ecg_create_analysis(ecg_id=ecg_id,
                             zero_crosses_count=zero_crosses_count)


@celery_app.task
def async_ecg_update_analysis_by_id(ecg_id: UUID):
    crud.ecg_update_analysed_by_id(ecg_id)

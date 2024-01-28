import logging
from uuid import UUID

from fastapi import APIRouter, Depends, status, HTTPException
from pydantic import UUID4

import src.db.crud as crud
from src.api.v1.auth.auth import authenticate_user
from src.celery.tasks import async_analyze_ecg_leads
from src.schemas import ECGSubmission, ECGAPIAsyncResponse, ECGAPIResponse

logger = logging.getLogger(__name__)

router = APIRouter(prefix='/ecg',
                   tags=['ecg'])


@router.post('', response_model=ECGAPIAsyncResponse)
async def submit_ecg(ecg: ECGSubmission,
                     user_id: UUID = Depends(authenticate_user)):

    async_analyze_ecg_leads.delay(ecg=ecg, user_id=user_id)

    return ECGAPIAsyncResponse(id=ecg.id,
                               message='ECG successfully submitted')


@router.get('/{ecg_id}', response_model=ECGAPIResponse)
async def get_ecg(ecg_id: UUID4,
                  user_id: UUID = Depends(authenticate_user)):

    ecg = crud.ecg_get_by_id_and_user_id(ecg_id, user_id=user_id)
    if ecg is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'ECG Analysis with ID: {ecg_id} and User ID: {user_id} not found.')

    if not ecg.analysed:
        return ECGAPIResponse(id=ecg_id, message='ECG is being analysed. Please wait...')

    ecg_analysis = crud.ecg_get_analysis_by_id(ecg_id)
    zero_crosses_count = ecg_analysis.zero_crosses_count

    return ECGAPIResponse(id=ecg_id,
                          zero_crosses_count=zero_crosses_count)

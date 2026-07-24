from app.models.move import Move
from app.models.user import User
from app.models.game import Game
from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from datetime import datetime
from app.database.base import Base
import sys
from app.database.crud import get_user, save_insight, clear_insights
from app.services.pattern_detector import compute_phase_blunder_rates, compute_opening_performance
from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from datetime import datetime
from app.database.base import Base

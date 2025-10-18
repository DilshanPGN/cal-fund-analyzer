"""
API Routes - RESTful endpoints for the CAL Fund Analyzer.
Implements the Controller Pattern for handling HTTP requests.
"""

from flask import Blueprint, jsonify, request
from datetime import datetime
import logging

from services import CALAPIService
from config import get_config

# Set up logging
logger = logging.getLogger(__name__)

# Create API blueprint
api_bp = Blueprint('api', __name__, url_prefix='/api')

# Initialize service
config = get_config('development')
cal_service = CALAPIService(config)


@api_bp.route('/funds', methods=['GET'])
def get_fund_rates():
    """
    GET /api/funds?date=YYYY-MM-DD
    
    Fetch fund rates for a specific date.
    
    Query Parameters:
        date (str): Date in YYYY-MM-DD format. Defaults to today.
        
    Returns:
        JSON response with fund data or error message
        
    Status Codes:
        200: Success
        400: Bad request (invalid date format)
        500: Server error
    """
    try:
        # Get and validate date parameter
        date = request.args.get('date', datetime.now().strftime('%Y-%m-%d'))
        
        if not cal_service.validate_date(date):
            return jsonify({
                'error': 'Invalid date format. Use YYYY-MM-DD',
                'example': '2024-10-18'
            }), 400
        
        # Fetch fund rates
        data = cal_service.fetch_fund_rates(date)
        
        if data is None:
            return jsonify({
                'error': 'Failed to fetch fund data',
                'date': date
            }), 500
        
        return jsonify(data), 200
        
    except Exception as e:
        logger.error(f"Error in get_fund_rates: {str(e)}")
        return jsonify({
            'error': str(e),
            'message': 'An error occurred while fetching fund data'
        }), 500


@api_bp.route('/funds/available', methods=['GET'])
def get_available_funds():
    """
    GET /api/funds/available
    
    Get list of all available funds.
    
    Returns:
        JSON response with list of fund names
        
    Status Codes:
        200: Success
        500: Server error
    """
    try:
        funds = cal_service.get_available_funds()
        
        return jsonify({
            'funds': funds,
            'count': len(funds),
            'timestamp': datetime.now().isoformat()
        }), 200
        
    except Exception as e:
        logger.error(f"Error in get_available_funds: {str(e)}")
        return jsonify({
            'error': str(e),
            'message': 'Failed to fetch available funds'
        }), 500


@api_bp.route('/health', methods=['GET'])
def health_check():
    """
    GET /api/health
    
    Health check endpoint to verify API status.
    
    Returns:
        JSON response with health status
        
    Status Codes:
        200: Service healthy
        503: Service unhealthy
    """
    health_status = cal_service.health_check()
    
    status_code = 200 if health_status['status'] == 'healthy' else 503
    
    return jsonify(health_status), status_code


@api_bp.errorhandler(404)
def not_found(error):
    """Handle 404 errors."""
    return jsonify({
        'error': 'Endpoint not found',
        'message': 'The requested API endpoint does not exist'
    }), 404


@api_bp.errorhandler(500)
def internal_error(error):
    """Handle 500 errors."""
    return jsonify({
        'error': 'Internal server error',
        'message': 'An unexpected error occurred'
    }), 500


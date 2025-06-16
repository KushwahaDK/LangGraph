"""Tool definitions for the multi-agent system."""

from .music_tools import (
    get_albums_by_artist,
    get_tracks_by_artist,
    get_songs_by_genre,
    check_for_songs,
    get_music_tools,
)
from .invoice_tools import (
    get_invoices_by_customer_sorted_by_date,
    get_invoices_sorted_by_unit_price,
    get_employee_by_invoice_and_customer,
    get_invoice_tools,
)

__all__ = [
    # Individual tools
    get_albums_by_artist,
    get_tracks_by_artist,
    get_songs_by_genre,
    check_for_songs,
    get_invoices_by_customer_sorted_by_date,
    get_invoices_sorted_by_unit_price,
    get_employee_by_invoice_and_customer,
    # Tool collections
    get_music_tools,
    get_invoice_tools,
]

from flask import Flask, request, jsonify
from connect_with_db import get_cursor

def start():
    """
    Entry point for Julian's module.
    Decides which insight to run, based on query parameters.
    returns a Flask Response (JSON)
    """
    mode = request.args.get('mode', "overview")

    if mode == "overview":
        return overall_by_province()
    
    elif mode == "by_province":
        provincie = request.args.get('provincie')
        if not provincie:
            return jsonify({"error": "Missing 'provincie' parameter"}), 400
        return education_by_province(provincie)
    
    elif mode == "top_for_education":
        onderwijssoort = request.args.get('onderwijssoort')
        if not onderwijssoort:
            return jsonify({"error": "Missing 'onderwijssoort' parameter"}), 400
        return top_provinces_for_education(onderwijssoort)
    
    elif mode == "myth_higher_edu":
        return myth_higher_education()
    
    else:
        return jsonify({"error": f"Unknown mode: {mode}"}), 400

def run_query(sql, params=None):
    """
    Opens a database connection, runs the given SQL query with optional parameters,
    returns rows as list of dicts, and then closes the connection.
    """
    conn, cursor = get_cursor()
    try:
        cursor.execute(sql, params or ())
        rows = cursor.fetchall()
        return rows
    finally:
        cursor.close()
        conn.close()

def overall_by_province():
    sql = """
    SELECT provincie, SUM(Aantal) AS totaal
    FROM gediplomeerden
    GROUP BY provincie
    ORDER BY totaal DESC;
    """
    rows = run_query(sql)
    return jsonify(rows)

def education_by_province(provincie):
    sql = """
    SELECT onderwijssoort, aantal
    FROM gediplomeerden_clean
    WHERE provincie = %s
    ORDER BY aantal DESC;
    """
    rows = run_query(sql, (provincie,))
    return jsonify(rows)

def top_provinces_for_education(onderwijssoort):
    sql = """
    SELECT provincie, aantal
    FROM gediplomeerden_clean
    WHERE onderwijssoort = %s
    ORDER BY aantal DESC
    LIMIT 5;
    """
    rows = run_query(sql, (onderwijssoort,))
    return jsonify(rows)

def myth_higher_education():
    sql = """
        SELECT 
            provincie,
            ROUND(
                SUM(CASE 
                    WHEN onderwijssoort LIKE 'HBO%' 
                      OR onderwijssoort LIKE 'WO%' 
                    THEN aantal 
                    ELSE 0 
                END) 
                /
                SUM(aantal) * 100, 
                2
            ) AS percentage_higher_edu
        FROM gediplomeerden_clean
        GROUP BY provincie
        ORDER BY percentage_higher_edu DESC;
    """
    rows = run_query(sql)
    return jsonify(rows)
CREATE OR REPLACE FUNCTION public.insert_event(
    p_match_id      INT,
    p_team          TEXT,
    p_player_number TEXT,
    p_event         TEXT,
    p_quarter       TEXT,
    p_time          TEXT,
    p_result        TEXT
)
RETURNS void AS $$
DECLARE
    v_team_id   INT;
    v_player_id INT;
BEGIN
    -- Resolve team_id from match
    IF p_team = 'team1' THEN
        SELECT team1_id INTO v_team_id FROM public.matches WHERE id = p_match_id;
    ELSE
        SELECT team2_id INTO v_team_id FROM public.matches WHERE id = p_match_id;
    END IF;

    IF v_team_id IS NULL THEN
        RAISE EXCEPTION 'Could not resolve team_id for match % and team %', p_match_id, p_team;
    END IF;

    -- Resolve player_id from number (nullable)
    IF p_player_number IS NOT NULL THEN
        SELECT id INTO v_player_id
        FROM public.players
        WHERE team_id = v_team_id AND number::text = p_player_number;
    END IF;

    -- Insert event
    INSERT INTO public.events (match_id, team_id, player_id, event, quarter, time, result)
    VALUES (p_match_id, v_team_id, v_player_id, p_event, p_quarter, p_time, p_result);
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION public.update_score(
  p_match_id INT,
  p_team TEXT
)
RETURNS void AS $$
BEGIN
  IF p_team = 'team1' THEN
    UPDATE public.matches SET team1_score = team1_score + 1 WHERE id = p_match_id;
  ELSE
    UPDATE public.matches SET team2_score = team2_score + 1 WHERE id = p_match_id;
  END IF;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION public.update_starter(
  p_team_id INT,
  p_number_out INT,
  p_number_in INT
)
RETURNS void AS $$
BEGIN
  UPDATE public.players SET starter = FALSE
  WHERE team_id = p_team_id AND number = p_number_out;

  UPDATE public.players SET starter = TRUE
  WHERE team_id = p_team_id AND number = p_number_in;
END;
$$ LANGUAGE plpgsql;
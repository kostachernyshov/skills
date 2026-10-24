#!/usr/bin/env python3
"""Tests for the harness. Run: python3 tests/harness/test_harness.py"""
import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from run_scenario import CUT, LIMIT, REPEAT, persona_answer, persona_limit_entry, resume_point  # noqa: E402


def fake_run(text):
    return lambda args, cwd, log_path, prompt: ({"result": text}, None, 0)


class PersonaLimit(unittest.TestCase):
    def test_limit_message_never_reaches_the_agent(self):
        self.assertIsNone(persona_answer("rules", "Q1?", "m", "/tmp", 1, run=fake_run(LIMIT + " · resets 5pm")))

    def test_normal_answer(self):
        self.assertEqual(persona_answer("rules", "Q1?", "m", "/tmp", 1, run=fake_run(" yes ")), "yes")

    def test_resume_after_persona_limit_repeats_the_question(self):
        old = [{"turn": 1, "step": 0, "prompt": "/a", "reply": "Q1?"}, persona_limit_entry(1, 0)]
        kept, step, prompt = resume_point(old)
        self.assertEqual(([t["turn"] for t in kept], step, prompt), ([1], 0, REPEAT))

    def test_resume_after_agent_limit_continues_the_step(self):
        old = [{"turn": 1, "step": 0, "prompt": "/a", "reply": "ok"},
               {"turn": 2, "step": 1, "prompt": "/b", "reply": LIMIT}]
        kept, step, prompt = resume_point(old)
        self.assertEqual(([t["turn"] for t in kept], step, prompt), ([1], 1, "/b" + CUT))


if __name__ == "__main__":
    unittest.main()

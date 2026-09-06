from pathlib import Path
import unittest


WORKFLOW = Path(".github/workflows/track-a-surveyor-v2-readonly.yml")


class SurveyorOwnerCommentTriggerContractTests(unittest.TestCase):
    def test_owner_comment_trigger_is_actor_preserving_and_fail_closed(self) -> None:
        source = WORKFLOW.read_text(encoding="utf-8")
        self.assertIn("issue_comment:", source)
        self.assertIn("github.event.issue.pull_request", source)
        self.assertIn("github.event.comment.user.login == github.repository_owner", source)
        self.assertIn(
            "startsWith(github.event.comment.body, '/track-a-surveyor-v2-readonly ONE_SHOT_SURVEYOR_READ_ONLY ')",
            source,
        )
        self.assertIn("id: request", source)
        self.assertIn("EVENT_NAME: ${{ github.event_name }}", source)
        self.assertIn("DISPATCH_AUTHORIZATION: ${{ inputs.authorization || '' }}", source)
        self.assertIn("DISPATCH_RUNTIME_TASK_ID: ${{ inputs.runtime_task_id || '' }}", source)
        self.assertIn("COMMENT_BODY: ${{ github.event.comment.body || '' }}", source)
        self.assertEqual(
            source.count("RUNTIME_TASK_ID: ${{ steps.request.outputs.runtime_task_id }}"),
            2,
        )
        self.assertNotIn("actions: write", source)
        self.assertNotIn("/dispatches", source)
        self.assertNotIn("GH_TOKEN", source)


if __name__ == "__main__":
    unittest.main()

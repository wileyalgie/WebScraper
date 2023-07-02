var tasks = context.Tasks
    .Where(t => CompletionStatus == null ||
                (CompletionStatus == CompletionStatus.Completed && t.CompletionDate != null) ||
                (CompletionStatus == CompletionStatus.NotCompleted && t.CompletionDate == null))
    .ToList();
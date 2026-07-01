namespace HRMS.SharedKernel;

/// <summary>
/// Lightweight result type for operations that can succeed or fail without throwing.
/// </summary>
public class Result
{
    protected Result(bool isSuccess, ResultError? error)
    {
        if (isSuccess && error is not null)
            throw new InvalidOperationException("A successful result cannot carry an error.");
        if (!isSuccess && error is null)
            throw new InvalidOperationException("A failed result must carry an error.");

        IsSuccess = isSuccess;
        Error = error;
    }

    public bool IsSuccess { get; }
    public bool IsFailure => !IsSuccess;
    public ResultError? Error { get; }

    public static Result Success() => new(true, null);
    public static Result Failure(ResultError error) => new(false, error);

    public static Result<TValue> Success<TValue>(TValue value) => new(value, true, null);
    public static Result<TValue> Failure<TValue>(ResultError error) => new(default, false, error);
}

/// <summary>Result carrying a value on success.</summary>
public sealed class Result<TValue> : Result
{
    private readonly TValue? _value;

    internal Result(TValue? value, bool isSuccess, ResultError? error)
        : base(isSuccess, error) => _value = value;

    public TValue Value => IsSuccess
        ? _value!
        : throw new InvalidOperationException("Cannot access the value of a failed result.");
}

/// <summary>A machine-readable error code plus a human-readable message.</summary>
public sealed record ResultError(string Code, string Message)
{
    public static readonly ResultError None = new(string.Empty, string.Empty);
}

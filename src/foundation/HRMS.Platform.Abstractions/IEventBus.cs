namespace HRMS.Platform.Abstractions;

/// <summary>
/// Publishes integration events across module boundaries. The concrete implementation is
/// outbox-backed (transactional write, reliable delivery via RabbitMQ) — see ADR-009 and
/// the Event Bus module. Provider is swappable behind this seam (ADR-027).
/// </summary>
public interface IEventBus
{
    Task PublishAsync<TEvent>(TEvent integrationEvent, CancellationToken cancellationToken = default)
        where TEvent : IntegrationEvent;
}

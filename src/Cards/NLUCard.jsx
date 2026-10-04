import { Brain, Sparkles } from "lucide-react";
import AgentCard from "./AgentCard";

function InfoRow({ label, value }) {
  if (value === null || value === undefined || value === "") {
    return null;
  }

  return (
    <div className="flex justify-between py-3 border-b border-slate-800">
      <span className="text-slate-400 capitalize">
        {label.replace(/_/g, " ")}
      </span>

      <span className="text-white font-medium">
        {value}
      </span>
    </div>
  );
}

export default function NLUCard({ data }) {
  // Backend NLU response:
  // {
  //   intent: "...",
  //   confidence: 0.9,
  //   entities: {...},
  //   missing_fields: [...]
  // }

  const nlu = data || {};
  const entities = nlu.entities || {};

  const confidence = Number(nlu.confidence) || 0;
  const missingFields = nlu.missing_fields || [];

  return (
    <AgentCard
      icon={<Brain size={22} />}
      title="Understanding Request"
      subtitle="Natural language understanding"
      status="completed"
    >
      {/* Intent */}
      {nlu.intent && (
        <div className="mb-4">
          <div className="text-slate-400 text-sm mb-1">
            Intent
          </div>

          <div className="text-white font-semibold capitalize">
            {nlu.intent.replace(/_/g, " ")}
          </div>
        </div>
      )}

      {/* Entities */}
      <div className="space-y-1">
        <InfoRow
          label="destination"
          value={entities.destination}
        />

        <InfoRow
          label="source"
          value={entities.source}
        />

        <InfoRow
          label="duration"
          value={
            entities.duration_days
              ? `${entities.duration_days} days`
              : null
          }
        />

        <InfoRow
          label="budget"
          value={
            entities.budget !== null &&
            entities.budget !== undefined
              ? `₹${Number(entities.budget).toLocaleString()}`
              : null
          }
        />

        <InfoRow
          label="travelers"
          value={entities.travelers}
        />

        <InfoRow
          label="travel style"
          value={entities.travel_style}
        />

        <InfoRow
          label="trip type"
          value={entities.trip_type}
        />

        <InfoRow
          label="start date"
          value={entities.start_date}
        />

        <InfoRow
          label="end date"
          value={entities.end_date}
        />

        <InfoRow
          label="interests"
          value={
            Array.isArray(entities.interests) &&
            entities.interests.length > 0
              ? entities.interests.join(", ")
              : null
          }
        />
      </div>

      {/* Confidence */}
      <div className="mt-6">
        <div className="flex justify-between mb-2 text-sm">
          <span className="text-slate-400">
            Confidence
          </span>

          <span className="text-white">
            {Math.round(confidence * 100)}%
          </span>
        </div>

        <div className="h-2 rounded-full bg-slate-800 overflow-hidden">
          <div
            className="h-full rounded-full bg-gradient-to-r from-blue-500 to-cyan-400"
            style={{
              width: `${Math.min(confidence * 100, 100)}%`,
            }}
          />
        </div>
      </div>

      {/* Missing fields */}
      {missingFields.length > 0 && (
        <div className="mt-6">
          <div className="text-slate-300 font-medium mb-3">
            Missing information
          </div>

          <div className="flex flex-wrap gap-2">
            {missingFields.map((field) => (
              <span
                key={field}
                className="px-3 py-1 rounded-full text-sm bg-amber-500/10 border border-amber-500/20 text-amber-300"
              >
                {field.replace(/_/g, " ")}
              </span>
            ))}
          </div>
        </div>
      )}

      {/* Final response */}
      <div className="mt-6 p-4 rounded-2xl bg-slate-950/60 border border-slate-800">
        <div className="flex items-center gap-2 text-blue-300">
          <Sparkles className="w-4 h-4" />

          <span className="text-sm">
            {data?.final_response ||
              "Request understood successfully."}
          </span>
        </div>
      </div>
    </AgentCard>
  );
}
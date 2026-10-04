import {
Map,
CalendarDays,
Wallet,
MapPin,
CircleCheck,
Sparkles,
Plane,
Palmtree,
} from "lucide-react";
import AgentCard from "./AgentCard";

function Metric({ icon, label, value, accent }) {
return (
<div className={`rounded-2xl border ${accent} bg-slate-900/70 p-5`}>
<div className="flex items-center gap-2 text-sm text-slate-400">
{icon}
{label}
</div>
<div className="mt-3 text-3xl font-bold text-white">{value}</div>
</div>
);
}

function DayCard({ day }) {
return (
<div className="relative overflow-hidden rounded-3xl border border-slate-800 bg-slate-900/70">
<div className="absolute left-0 top-0 h-full w-1 bg-gradient-to-b from-blue-500 to-cyan-400" />

  <div className="p-6">
    <div className="flex items-start justify-between">
      <div>
        <div className="inline-flex items-center rounded-full border border-blue-500/20 bg-blue-500/10 px-3 py-1 text-sm font-medium text-blue-300">
          Day {day.day}
        </div>

        <h3 className="mt-3 text-xl font-semibold text-white">
          {day.title}
        </h3>
      </div>

      <div className="rounded-2xl border border-emerald-500/20 bg-emerald-500/10 px-4 py-2 text-right">
        <div className="text-xs uppercase tracking-wide text-emerald-300">
          Estimated
        </div>
        <div className="text-lg font-bold text-white">
          {day.estimated_cost != null
            ? `₹${day.estimated_cost.toLocaleString()}`
            : "Budget pending"}
        </div>
      </div>
    </div>

    <div className="mt-6 space-y-4">
      {(day.activities || []).map((activity, index) => (
        <div
          key={index}
          className="flex items-start gap-3 rounded-xl bg-slate-800/40 p-3"
        >
          <CircleCheck className="mt-0.5 h-5 w-5 flex-shrink-0 text-cyan-400" />
          <p className="leading-relaxed text-slate-200">{activity}</p>
        </div>
      ))}
    </div>
  </div>
</div>

);
}

export default function PlannerCard({ data }) {
const planner =
data?.planner ||
data?.agent_outputs?.planner ||
data;

if (!planner) return null;

return (
<AgentCard
icon={<Map size={22} />}
title={`${planner.destination || "Trip"} itinerary`}
subtitle="Optimized day-by-day travel plan"
status="completed"
>
{/* Hero metrics */}
<div className="grid gap-4 md:grid-cols-3">
<Metric
icon={<MapPin className="h-5 w-5 text-blue-400" />}
label="Destination"
value={planner.destination || "Not specified"}
accent="border-blue-500/20"
/>

    <Metric
      icon={<CalendarDays className="h-5 w-5 text-cyan-400" />}
      label="Duration"
      value={
        planner.duration_days
          ? `${planner.duration_days} days`
          : "Not specified"
      }
      accent="border-cyan-500/20"
    />

    <Metric
      icon={<Wallet className="h-5 w-5 text-emerald-400" />}
      label="Total estimated cost"
      value={
        planner.total_estimated_cost != null
          ? `₹${planner.total_estimated_cost.toLocaleString()}`
          : "To be calculated"
      }
      accent="border-emerald-500/20"
    />
  </div>

  {/* Route banner */}
  <div className="mt-6 rounded-2xl border border-slate-800 bg-gradient-to-r from-blue-900/30 to-cyan-900/20 p-5">
    <div className="flex items-center gap-3">
      <Plane className="h-5 w-5 text-blue-300" />
      <div>
        <div className="text-sm text-slate-400">Travel route</div>
        <div className="text-lg font-semibold text-white">
          {planner.destination
            ? `Explore ${planner.destination} across ${planner.duration_days || "multiple"} days`
            : "Personalized travel route"}
        </div>
      </div>
    </div>
  </div>

  {/* Itinerary */}
  {Array.isArray(planner.day_plans) && planner.day_plans.length > 0 && (
    <div className="mt-8">
      <div className="mb-5 flex items-center gap-2">
        <Sparkles className="h-5 w-5 text-cyan-400" />
        <h3 className="text-lg font-semibold text-white">
          Highlighted itinerary
        </h3>
      </div>

      <div className="space-y-5">
        {planner.day_plans.map((day) => (
          <DayCard key={day.day} day={day} />
        ))}
      </div>
    </div>
  )}

  {/* Featured insight */}
  <div className="mt-8 rounded-3xl border border-blue-500/20 bg-gradient-to-r from-blue-950/60 to-cyan-950/40 p-6">
    <div className="mb-3 flex items-center gap-3">
      <Palmtree className="h-6 w-6 text-cyan-300" />
      <h4 className="text-xl font-semibold text-white">
        Travel insight
      </h4>
    </div>

    <p className="leading-relaxed text-slate-200">
      {planner.notes ||
        "This itinerary has been generated based on your destination and trip duration. Budget estimates can be refined once hotel preferences, flight options, and travel dates are finalized."}
    </p>
  </div>
</AgentCard>

);
}
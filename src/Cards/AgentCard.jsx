import { motion } from "framer-motion";
import { CheckCircle2, LoaderCircle, AlertCircle } from "lucide-react";

export default function AgentCard({
  icon,
  title,
  subtitle,
  status = "completed",
  children,
}) {
  const StatusIcon = () => {
    switch (status) {
      case "running":
        return <LoaderCircle className="w-5 h-5 text-blue-400 animate-spin" />;
      case "failed":
        return <AlertCircle className="w-5 h-5 text-red-400" />;
      default:
        return <CheckCircle2 className="w-5 h-5 text-emerald-400" />;
    }
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 24 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.35 }}
      className="relative mb-6"
    >
      <div className="absolute -inset-1 rounded-3xl bg-gradient-to-r from-blue-600/20 via-cyan-500/10 to-blue-600/20 blur-xl" />

      <div className="relative overflow-hidden rounded-3xl border border-slate-800 bg-slate-900/90 backdrop-blur-xl shadow-2xl">
        <div className="h-1 bg-gradient-to-r from-blue-500 via-cyan-400 to-blue-500" />

        <div className="flex items-center justify-between px-6 py-5 border-b border-slate-800">
          <div className="flex items-center gap-4">
            <div className="w-12 h-12 rounded-2xl bg-blue-600/20 border border-blue-500/20 flex items-center justify-center text-blue-400">
              {icon}
            </div>

            <div>
              <h3 className="text-white font-semibold text-lg">
                {title}
              </h3>
              <p className="text-slate-400 text-sm">
                {subtitle}
              </p>
            </div>
          </div>

          <StatusIcon />
        </div>

        <div className="p-6">{children}</div>
      </div>
    </motion.div>
  );
}
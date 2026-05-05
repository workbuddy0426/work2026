"""
asset_allocator.py - 第4章：资产配置与风险管理 Python 实现
包含: 马克维茨均值-方差 / 切线组合 / 风险平价 / 带约束优化
"""

import numpy as np
import pandas as pd
from typing import Optional, Tuple

class PortfolioOptimizer:
    """
    资产配置优化器
    
    示例: 3只资产
    mu = [0.12, 0.08, 0.06]   # 预期收益
    sigma = [0.20, 0.15, 0.10] # 波动率
    corr = [[1.00, 0.25, 0.10],   # 相关系数矩阵
            [0.25, 1.00, 0.30],
            [0.10, 0.30, 1.00]]
    """

    def __init__(self, mu: list, sigma: list, corr: list, rf: float = 0.04):
        """
        mu: 各资产预期年化收益 (list)
        sigma: 各资产年化波动率 (list)
        corr: 相关系数矩阵 (n x n)
        rf: 无风险利率 (default 4%)
        """
        self.n = len(mu)
        self.mu = np.array(mu)
        self.rf = rf
        
        # 从sigma和corr构造协方差矩阵
        sigma_arr = np.array(sigma)
        corr_mat = np.array(corr)
        self.Sigma = np.outer(sigma_arr, sigma_arr) * corr_mat
        
        # 验证输入
        assert self.Sigma.shape == (self.n, self.n), "协方差矩阵维度不匹配"
        assert np.allclose(self.Sigma, self.Sigma.T), "协方差矩阵必须对称"
    
    # ======= 1. 组合统计量 =======

    def portfolio_stats(self, w: np.ndarray) -> dict:
        """计算给定权重的组合统计量"""
        w = np.array(w)
        ret = w @ self.mu
        var = w @ self.Sigma @ w
        std = np.sqrt(var)
        sharpe = (ret - self.rf) / std if std > 0 else 0
        return {'ret': ret, 'std': std, 'var': var, 'sharpe': sharpe}
    
    # ======= 2. 马克维茨均值-方差 =======

    def min_variance(self, target_ret: Optional[float] = None) -> Tuple[np.ndarray, dict]:
        """
        目标: min w'Sw 
        约束: w'1=1, w'u=target_ret (如果给定), w>=0
        
        返回: (最优权重, 统计量)
        """
        from scipy.optimize import minimize
        
        def obj_func(w):
            return w @ self.Sigma @ w
        
        constraints = [{'type': 'eq', 'fun': lambda w: w.sum() - 1}]
        if target_ret is not None:
            constraints.append({'type': 'eq', 'fun': lambda w: w @ self.mu - target_ret})
        
        bounds = [(0, 1)] * self.n  # 默认不加杠杆
        x0 = np.ones(self.n) / self.n
        
        result = minimize(obj_func, x0, 
                         method='SLSQP',
                         bounds=bounds,
                         constraints=constraints,
                         options={'ftol': 1e-12, 'maxiter': 1000})
        
        w_opt = result.x
        
        # 如果没给target_ret, 返回的是全局最小方差组合
        return w_opt, self.portfolio_stats(w_opt)
    
    def efficient_frontier(self, n_points: int = 50) -> pd.DataFrame:
        """
        生成有效前沿上的n_points个组合
        从最小方差组合扫描到最大收益组合
        """
        # 先找最小方差和最大收益
        w_minvar, _ = self.min_variance()
        ret_minvar = self.portfolio_stats(w_minvar)['ret']
        
        # 最大收益组合 = 全部投在收益最高的资产上
        idx_max = np.argmax(self.mu)
        w_maxret = np.zeros(self.n)
        w_maxret[idx_max] = 1
        ret_maxret = self.mu[idx_max]
        
        # 在[ret_minvar, ret_maxret]之间均匀取点
        targets = np.linspace(ret_minvar, ret_maxret * 0.999, n_points)
        
        frontier = []
        for target in targets:
            try:
                w, stats = self.min_variance(target_ret=target)
                frontier.append({'ret': stats['ret'], 'std': stats['std'], 
                                'sharpe': stats['sharpe'], 'weights': w})
            except:
                continue
        
        return pd.DataFrame(frontier)
    
    # ======= 3. 切线组合 (最大夏普) =======

    def tangency_portfolio(self) -> Tuple[np.ndarray, dict]:
        """
        最大化夏普比率: max (w'u - rf) / sqrt(w'Sw)
        约束: w'1=1, w>=0
        
        返回: (切线组合权重, 统计量)
        """
        from scipy.optimize import minimize
        
        def neg_sharpe(w):
            stats = self.portfolio_stats(w)
            return -stats['sharpe']
        
        constraints = [{'type': 'eq', 'fun': lambda w: w.sum() - 1}]
        bounds = [(0, 1)] * self.n
        x0 = np.ones(self.n) / self.n
        
        result = minimize(neg_sharpe, x0,
                         method='SLSQP',
                         bounds=bounds,
                         constraints=constraints,
                         options={'ftol': 1e-12, 'maxiter': 1000})
        
        w_opt = result.x
        return w_opt, self.portfolio_stats(w_opt)
    
    # ======= 4. 带交易成本惩罚的优化 =======

    def with_transaction_cost(self, w_prev: np.ndarray, 
                              target_ret: float,
                              lambda_tc: float = 0.01) -> Tuple[np.ndarray, dict]:
        """
        在目标函数中加入换手率惩罚
        min w'Sw + lambda_tc * ||w - w_prev||^2
        约束: w'1=1, w'u >= target_ret, w>=0
        """
        from scipy.optimize import minimize
        
        def obj_func(w):
            var_cost = w @ self.Sigma @ w
            tc_cost = lambda_tc * np.sum((w - w_prev) ** 2)
            return var_cost + tc_cost
        
        constraints = [{'type': 'eq', 'fun': lambda w: w.sum() - 1},
                       {'type': 'ineq', 'fun': lambda w: w @ self.mu - target_ret}]
        bounds = [(0, 1)] * self.n
        x0 = w_prev  # 从当前持仓开始
        
        result = minimize(obj_func, x0,
                         method='SLSQP',
                         bounds=bounds,
                         constraints=constraints,
                         options={'ftol': 1e-12, 'maxiter': 1000})
        
        w_opt = result.x
        turnover = np.sum(np.abs(w_opt - w_prev)) / 2
        stats = self.portfolio_stats(w_opt)
        stats['turnover'] = turnover
        return w_opt, stats
    
    # ======= 5. 风险平价 =======

    def risk_parity(self) -> Tuple[np.ndarray, dict]:
        """
        风险平价: 每个资产对组合总风险的贡献相等
        RC_i = w_i * (Sw)_i / sqrt(w'Sw)
        目标: 所有RC_i相等
        
        使用数值求解
        """
        from scipy.optimize import minimize
        
        def risk_parity_obj(w):
            w = np.array(w)
            if np.any(w < 0):
                return 1e10
            port_var = w @ self.Sigma @ w
            port_std = np.sqrt(port_var)
            if port_std < 1e-10:
                return 1e10
            # 各资产风险贡献
            mcr = self.Sigma @ w / port_std
            rc = w * mcr
            # 目标是所有RC相等 -> 最小化方差
            target_rc = port_std / self.n
            return np.sum((rc - target_rc) ** 2)
        
        constraints = [{'type': 'eq', 'fun': lambda w: w.sum() - 1}]
        bounds = [(0, 1)] * self.n
        x0 = np.ones(self.n) / self.n
        
        result = minimize(risk_parity_obj, x0,
                         method='SLSQP',
                         bounds=bounds,
                         constraints=constraints,
                         options={'ftol': 1e-12, 'maxiter': 2000})
        
        w_opt = result.x
        return w_opt, self.portfolio_stats(w_opt)
    
    # ======= 6. 带集中度限制的优化 =======

    def with_concentration_limit(self, max_weight: float = 0.2) -> Tuple[np.ndarray, dict]:
        """
        加集中度限制的切线组合
        单标的上限为 max_weight
        """
        from scipy.optimize import minimize
        
        def neg_sharpe(w):
            return -self.portfolio_stats(w)['sharpe']
        
        constraints = [{'type': 'eq', 'fun': lambda w: w.sum() - 1}]
        bounds = [(0, max_weight)] * self.n
        x0 = np.ones(self.n) / self.n
        
        result = minimize(neg_sharpe, x0,
                         method='SLSQP',
                         bounds=bounds,
                         constraints=constraints,
                         options={'ftol': 1e-12, 'maxiter': 1000})
        
        return result.x, self.portfolio_stats(result.x)


# ======= 运行demo =======

if __name__ == '__main__':
    print("=" * 60)
    print("第4章 Demo: 资产配置优化器")
    print("=" * 60)
    
    # 3只资产: AI题材 / 消费蓝筹 / 债券
    mu = [0.15, 0.10, 0.05]
    sigma = [0.25, 0.18, 0.06]
    corr = [[1.00, 0.30, 0.05],
            [0.30, 1.00, 0.15],
            [0.05, 0.15, 1.00]]
    
    opt = PortfolioOptimizer(mu, sigma, corr, rf=0.04)
    
    # 1. 等权组合
    w_equal = np.ones(3) / 3
    s_equal = opt.portfolio_stats(w_equal)
    
    # 2. 最小方差
    w_minvar, s_minvar = opt.min_variance()
    
    # 3. 切线组合
    w_tang, s_tang = opt.tangency_portfolio()
    
    # 4. 风险平价
    w_rp, s_rp = opt.risk_parity()
    
    # 5. 带集中度限制
    w_conc, s_conc = opt.with_concentration_limit(max_weight=0.5)
    
    # 6. 带交易成本惩罚
    w_prev = w_equal
    w_tc, s_tc = opt.with_transaction_cost(w_prev, target_ret=0.10, lambda_tc=0.02)
    
    # 汇总对比
    results = pd.DataFrame({
        '等权组合': [s_equal['ret'], s_equal['std'], s_equal['sharpe']] + list(w_equal),
        '最小方差': [s_minvar['ret'], s_minvar['std'], s_minvar['sharpe']] + list(w_minvar),
        '切线组合': [s_tang['ret'], s_tang['std'], s_tang['sharpe']] + list(w_tang),
        '风险平价': [s_rp['ret'], s_rp['std'], s_rp['sharpe']] + list(w_rp),
        '限集中度': [s_conc['ret'], s_conc['std'], s_conc['sharpe']] + list(w_conc),
    }, index=['收益', '风险', '夏普', 
              'AI题材权重', '消费蓝筹权重', '债券权重'])
    
    results = results.round(4)
    
    print("\n五种策略对比:")
    print(results.to_string())
    
    print(f"\n{'='*60}")
    print(f"切线组合T = AI:{w_tang[0]:.1%}, 消费:{w_tang[1]:.1%}, 债券:{w_tang[2]:.1%}")
    print(f"夏普比率 = {s_tang['sharpe']:.3f}")
    print(f"\n注意风险平价的结果: 债券占比最高")
    print(f"因为它的波动最小, 风险平价会给它最大权重来平衡风险贡献")
